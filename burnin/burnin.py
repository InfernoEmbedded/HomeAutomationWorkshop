#!/usr/bin/python

import argparse
import json
import os
import re
import requests
import serial
import sys


COMMANDS = ['ip address',
            'sudo owhttpd --debug --i2c=/dev/i2c-0:18 -p 80']


def index_of(lines, elem):
    idx = 0
    for line in lines:
        if line.find(elem) != -1:
            return idx
        idx += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('serialport')
    parser.add_argument('--verbose', help='Be more chatty',
                        action='store_true')
    parser.add_argument('--username', help='Username to login as')
    parser.add_argument('--password', help='Password for that user')
    parser.add_argument('--board', help='The index into the board listing')
    args = parser.parse_args()

    if os.path.exists('boards.json'):
        with open('boards.json') as f:
            boards = json.loads(f.read())
    else:
        boards = {}
    boards.setdefault(args.board, {})

    ser = serial.Serial(args.serialport, 115200, timeout=1)

    def send(ser, s):
        print('[out] %s' % s)
        ser.write(s.encode('utf-8'))
        ser.write('\n'.encode('utf-8'))
    
    buf = ''
    delay = 0
    command = None
    command_output = []
    while True:
        data = ser.read(100)
        if len(data) == 0:
            delay += 1
        else:
            buf += data.decode('utf-8')
            delay = 0

        # Process complete lines
        if buf.find('\n') != 1:
            lines = buf.split('\n')

            for line in lines[:-1]:
                if args.verbose:
                    print('[in ] %s' % line)

                if command:
                    command_output.append(line)

            buf = lines[-1]

        # If we've been sitting for five seconds, then we're probably at a
        # prompt
        if delay > 4:
            print('[in>] %s' % buf)

            if len(buf) == 0:
                if command:
                    if command.startswith('sudo owhttpd '):
                        # We can now talk to the HTTP server and check that
                        # 1-Wire is working
                        url = ('http://%s/uncached'
                                % boards[args.board]['ip_address'])
                        print('[req] %s' % url)
                        r = requests.get(url)
                        if r.text.find('28.') != -1:
                            boards[args.board]['one_wire_local_found'] = True
                        else:
                            boards[args.board]['one_wire_local_found'] = False
                            print('Local 1-Wire device missing!')
                            sys.exit(1)

                        if r.text.find('ED.') != -1:
                            boards[args.board]['one_wire_remote_found'] = True
                        else:
                            boards[args.board]['one_wire_remote_found'] = False
                            print('Remote 1-Wire device missing!')
                            sys.exit(1)

                        # And then ctrl-c
                        ser.write(b'\x03')

                else:
                    send(ser, '')

            elif buf.startswith('orangepiprime login:'):
                send(ser, '%s' % args.username)
            elif buf.startswith('Password:'):
                send(ser, '%s' % args.password)
            elif buf.find(':~$') != -1:
                if command:
                    # We were runing a command, consider the output
                    print('--------------- command ------------------')
                    print(command)
                    print('--------------- output -------------------')
                    print('\n'.join(command_output))
                    print('--------------- analysis -----------------')

                    if command == 'ip address':
                        # We are learning the mac address of eth0
                        idx = index_of(command_output, '2: eth0')
                        r = re.compile(' +link/ether (.*) brd .*')
                        m = r.match(command_output[idx + 1])
                        if m:
                            ether = m.group(1)
                            print('eth0 mac address is %s' % ether)
                            boards[args.board]['mac_address'] = ether
                        else:
                            print('We didn\'t find a mac address! Aborting.')
                            sys.exit(1)

                        # Did we get link?
                        r = re.compile('.* qdisc .* state ([^ ]*) .*')
                        m = r.match(command_output[idx])
                        if m:
                            if m.group(1) == 'DOWN':
                                print('eth0 did not see link')
                                boards[args.board]['saw_link'] = False
                            else:
                                boards[args.board]['saw_link'] = True
                        else:
                            print('We didn\'t find link state! Aborting.')
                            sys.exit(1)

                        # Ensure we managed a DHCP correctly, but only if
                        # if we have link
                        if boards[args.board]['saw_link']:
                            r = re.compile('    inet ([^ ]+)/24 .*')
                            m = r.match(command_output[idx + 2])
                            if m:
                                boards[args.board]['got_address'] = True
                                boards[args.board]['ip_address'] = m.group(1)
                            else:
                                print('We didn\'t find an address! Aborting.')
                                sys.exit(1)

                    print('------------------------------------------')

                if len(COMMANDS) == 0:
                    print('...and we\'re done!')
                    with open('boards.json', 'w') as f:
                        f.write(json.dumps(boards, indent=4, sort_keys=True))
                    sys.exit(0)

                command = COMMANDS.pop(0)
                send(ser, command)

            buf = ''


if __name__ == '__main__':
    main()
