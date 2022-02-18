import os
import paramiko
import time
import getpass
import yaml


def error_log(error):
    log = open("log.txt", "a")
    log.write(error + "\n")
    log.close()

try:
    username = input("Input your username:").strip()
    password = getpass.getpass()
    directory = os.getcwd()


    try:
        hostname = open(directory + "\\Network_Devices.yml", "r")
        hostname_yml = yaml.load(hostname, Loader=yaml.FullLoader)
        hostname.close()

    except Exception as error:
        error_log(str(error))
        print(error)


    output_file = open("output_file.txt", "a")

    for categories in hostname_yml.keys():
        if "#" in categories[0]:

            pass
        elif hostname_yml[categories] == None:
            pass

        else:
            for devices in hostname_yml[categories]:
                if "#" in devices[0]:
                    pass
                elif hostname_yml[categories][devices] == None:
                    pass

                else:
                    hostname = hostname_yml[categories][devices]
                    try:
                        ssh_client = paramiko.SSHClient()
                        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        ssh_client.connect(hostname=hostname, username=username, password=password)
                        print("Successful connection to: ", hostname)
                        remote_connection = ssh_client.invoke_shell()
                        remote_connection.send("terminal leng 0\n")
                        try:
                            commands = open(directory + "\\commands.txt", "r")
                        except Exception as error:
                            error_log(str(error))
                            exit()
                        for command in commands:
                            remote_connection.send(command)
                            remote_connection.send("\n")
                            time.sleep(1)
                            output = remote_connection.recv(65535).decode()
                            print(output)
                            output_file.write(output)
                            time.sleep(1)

                        commands.close()

                        remote_connection.send("end\n")
                        remote_connection.send("wr\n")
                        remote_connection.send("exit\n")

                    except Exception as error:
                        error_log(str(error))
                        print(error)


    output_file.close()

except Exception as error:
    error_log(str(error))
    print(error)



while True:
    pass
