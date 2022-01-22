import urlscan
from threading import Thread


def main():
    str_input = input("Enter queries (separated by a commas): \n")
    queries = str_input.split(',')
    threads = []
    result = {key:[] for key in queries}
    for query in queries:
        t = Thread(target=urlscan.search_scans_by_query, args=(query, result[query]))
        threads.append(t)
        t.start()
    for thread in threads:
        thread.join()

    print(result)
    return result


if __name__ == "__main__":
    main()
