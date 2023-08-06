#!/usr/bin/env python
import docker
import time
import argparse


def run_docker(image, volumes, command, environment):
    client = docker.from_env()
    container = client.containers.run(image, command, volumes=volumes, detach=True, environment=environment)
    stats = container.stats(stream=True, decode=True)
    max_usage = .0
    max_usage_test = .0
    max_total_rss = .0

    while not container.status.startswith("e"):
        container.reload()
        next_stats = next(stats)
        # print json.dumps(next_stats, sort_keys=True, indent=4, separators=(',', ': '))
        time.sleep(1)
        try:
            max_usage = next_stats["memory_stats"]["max_usage"]
            usage = next_stats["memory_stats"]["usage"]
            if usage > max_usage_test:
                max_usage_test = usage
            total_rss = next_stats["memory_stats"]["stats"]["total_rss"]
            if total_rss > max_total_rss:
                max_total_rss = total_rss
        except KeyError:
            pass
    print "%f MB\t%f MB\t%f MB" % (max_usage / 1048576.0, max_usage_test / 1048576.0, max_total_rss / 1048576.0)

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image")
parser.add_argument("-v", "--volume", type=lambda x: x.split(":"), action="append")
parser.add_argument("-c", "--command")
parser.add_argument("-e", "--environment")
args = parser.parse_args()
if not args.image or not args.volume:
    parser.print_help()
    parser.exit(1)
if not args.command:
    run_command = None
else:
    run_command = args.command
volumes = dict()
for i in range(0, len(args.volume)):
    # print "%s %s %s" % (args.volume[i][0], args.volume[i][1], args.volume[i][2])
    if len(args.volume[0]) < 3:
        parser.print_help()
        exit(1)
    volumes[args.volume[i][0]] = {'bind': args.volume[i][1], 'mode': args.volume[i][2]}

#print volumes
#exit()
environment = None
if args.environment:
    environment = {'YAML': args.environment}

start_time = time.time()
run_docker(args.image, volumes, args.command, environment)
elapsed_time = time.time() - start_time
print "%.2fs or %.2fm or %.2fh" % (elapsed_time, elapsed_time/60, elapsed_time/3600)

