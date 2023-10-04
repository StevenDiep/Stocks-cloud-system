from jobs import q, update_job_status, return_job, rd, rdiimport matplotlib.pyplot as pltimport jsonfrom funcs import string_to_date_arr@q.workerdef working(jid):    update_job_status(jid, "In Progress")    job_data = return_job(jid)        if job_data["job_type"] == 'graph':        ticker = json.loads(job_data['input_values'])['ticker']        graph_data = json.loads(rd.get("Stocks"))[ticker]        x_values = string_to_date_arr(graph_data.keys())        y_values = graph_data.values()                plt.xlabel('Date')        plt.ylabel('Closing price')        plt.title(str(ticker))                plt.plot(x_values, y_values)        plt.savefig('output_img.png')                    with open('output_img.png', 'rb') as f:            img = f.read()            if job_data["job_type"] == 'compare':        ticker1 = json.loads(job_data['input_values'])['ticker1']        ticker2 = json.loads(job_data['input_values'])['ticker2']                graph_data1 = json.loads(rd.get("Stocks"))[ticker1]        x_values = string_to_date_arr(graph_data1.keys())        y1_values = graph_data1.values()                graph_data2 = json.loads(rd.get("Stocks"))[ticker2]        y2_values = graph_data2.values()                plt.xlabel('Date')        plt.ylabel('Closing Price')        plt.title(str(ticker1) + ' vs. ' + str(ticker2))        plt.legend()                plt.plot(x_values, y1_values)        plt.plot(x_values, y2_values)                plt.savefig('output_img.png')                with open('output_img.png', 'rb') as f:            img = f.read()                rdi.set('job.{}'.format(jid), img)      rd.hset('job.{}'.format(jid), 'status', 'finished')    working()