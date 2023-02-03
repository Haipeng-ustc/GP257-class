import multiprocessing
  
def process_function(lock):
    lock.acquire()
    # CRITICAL SECTION
    print("CRITICAL SECTION")
    print("Only One Process has to access at a given time")
    lock.release()

def run():
    lock = multiprocessing.Lock()
    process_1 = multiprocessing.Process(target=process_function, args=(lock,))
    process_2 = multiprocessing.Process(target=process_function, args=(lock,))
    process_1.start()
    process_2.start()
    process_1.join()
    process_2.join()

if __name__ == "__main__":
    run()
