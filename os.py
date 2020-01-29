import json, time, multiprocessing 

def calc_values(d, data, num):
        temps = []
        for hour in data:
            temps.append(hour["temperature"])

        temps = list(filter(None, temps))
        max_temp = max(temps)
        min_temp = min(temps)
        avg_temp = sum(temps)/len(temps)
        d[num] = [max_temp, min_temp, avg_temp]


if __name__ == '__main__': 

    with open('weatherdata.json') as json_file:
        data = json.load(json_file)

        start_time = time.perf_counter()
        temps = []
        for hour in data:
            temps.append(hour["temperature"])

        temps = list(filter(None, temps))
        print("_____WITHOUT MULTIPROCESSING____")
        print("MAX TEMP: " + str(max(temps)))
        print("MIN TEMP: " + str(min(temps)))
        print("AVG TEMP: " + str(round(sum(temps)/len(temps),4)))
        print("TIME: " + str(round(time.perf_counter() - start_time,4)) + "s")
        print("\n")

        # with multiprocessing
        d = multiprocessing.Manager().dict()
        split_pos = round(len(data)/4)

        p1 = multiprocessing.Process(target=calc_values, args=(d,data[:split_pos],0, )) 
        p2 = multiprocessing.Process(target=calc_values, args=(d,data[split_pos:(2*split_pos)],1, )) 
        p3 = multiprocessing.Process(target=calc_values, args=(d,data[(2*split_pos):(3*split_pos)],2, )) 
        p4 = multiprocessing.Process(target=calc_values, args=(d,data[(3*split_pos):],3, )) 

        p1.start()
        p2.start() 
        p3.start()
        p4.start() 

        start_time_multi = time.perf_counter()
    
        p1.join() 
        p2.join() 
        p3.join() 
        p4.join() 

        max_temp = max([d[0][0], d[1][0], d[2][0], d[3][0]])
        min_temp = min([d[0][1], d[1][1], d[2][1], d[3][1]])
        avg_temp = round((d[0][2] + d[1][2] + d[2][2] + d[3][2]) / 4, 4)

        end_time = time.perf_counter()
        print("_____WITH MULTIPROCESSING_____")
        print("MAX TEMP: " + str(max_temp))
        print("MIN TEMP: " + str(min_temp))
        print("AVG TEMP: " + str(avg_temp))
        print("TIME: " + str(round(end_time - start_time_multi,4)) + "s")