import urlscan


def main():
    quotas = urlscan.get_quotas()
    query = input("Enter queries (separated by a comma): \n")
    response = urlscan.search_scans_by_query(query)
    quotas = urlscan.get_quotas()


    if response.__class__ == str:
        print(response)
        return None
    else:
        return {'results': response}


if __name__ == "__main__":
    main()
