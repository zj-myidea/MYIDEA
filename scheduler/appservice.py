from service.service import Master

if __name__ == '__main__':
    master = Master()
    try:
        master.start()
    except Exception as e:
        master.shutdown()

