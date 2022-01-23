import urlscan
from threading import Thread
import time


def main():
    str_input = input("Enter queries (separated by a commas): \n")
    queries = str_input.split(',')
    result = {key: [] for key in queries}
    threads = []
    l = 0  # l represents the number of threads, except for the main

    while True:
        quotas = urlscan.get_quotas()
        if quotas['day'] == 0 or quotas['hour'] == 0:
            print("You have exceeded your hourly/daily limit, there might be partial results")
            break
        quota = min(quotas.values())
        for i in range(quota):
            t = Thread(target=urlscan.search_scans_by_query, args=(queries[l], result[queries[l]]))
            l += 1
            threads.append(t)
            t.start()
            if len(queries) == l:
                break
        if len(queries) == l:
            break
        time.sleep(60)

    for thread in threads:
        thread.join()

    return result


if __name__ == "__main__":
    main()
