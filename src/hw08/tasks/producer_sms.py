from hw08.tasks.producer import main


if __name__ == "__main__":
    main(max_records=5, prefer_type="type_sms", drop=False)
