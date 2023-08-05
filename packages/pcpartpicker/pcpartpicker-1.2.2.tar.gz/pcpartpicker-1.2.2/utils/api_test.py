from pcpartpicker.api import API


def main():
    api = API()
    api.set_concurrent_connections(25)
    api.set_multithreading(False)
    # parts = api.supported_parts
    # for part in parts:
    #     part_data = api.retrieve(part)
    parts = api.retrieve_all()
    print(parts)


if __name__ == "__main__":
    main()
