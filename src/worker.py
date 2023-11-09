from jobs import q, update_job_status, return_job, rd, rdi, rdsimport matplotlib.pyplot as pltimport jsonfrom funcs import string_to_date_arr, convert_values_to_diff@q.workerdef working(jid):    update_job_status(jid, "In Progress")    job_data = return_job(jid)        if job_data["job_type"] == 'graph':        ticker = json.loads(job_data['input_values'])['ticker']        graph_data = json.loads(rds.get(ticker))        x_values = string_to_date_arr(graph_data.keys())        y_values = graph_data.values()                plt.xlabel('Date')        plt.ylabel('Closing price')        plt.title(str(ticker))                plt.plot(x_values, y_values)        plt.savefig('output_img.png')        plt.clf()                    with open('output_img.png', 'rb') as f:            img = f.read()            if job_data["job_type"] == 'compare':        ticker1 = json.loads(job_data['input_values'])['ticker1']        ticker2 = json.loads(job_data['input_values'])['ticker2']                graph_data1 = json.loads(rds.get(ticker1))        x_values = string_to_date_arr(graph_data1.keys())        y1_values = graph_data1.values()                graph_data2 = json.loads(rds.get(ticker2))        y2_values = graph_data2.values()                plt.plot(x_values, y1_values, 'r', label=ticker1)        plt.plot(x_values, y2_values, 'b', label=ticker2)        plt.legend()                plt.xlabel('Date')        plt.ylabel('Closing Price')        plt.title(str(ticker1) + ' vs. ' + str(ticker2))                plt.savefig('output_img.png')        plt.clf()                with open('output_img.png', 'rb') as f:            img = f.read()        if job_data["job_type"] == 'sp500':        sp500 = '^GSPC'        ticker = json.loads(job_data['input_values'])['ticker']                graph_data1 = json.loads(rds.get(sp500))        graph_data2 = json.loads(rds.get(ticker))                x_values = string_to_date_arr(graph_data1.keys())        y1_values = convert_values_to_diff(graph_data1.values())        y2_values = convert_values_to_diff(graph_data2.values())                plt.plot(x_values, y1_values, 'r', label="SP500")        plt.plot(x_values, y2_values, 'b', label=ticker)        plt.legend()                plt.xlabel('Date')        plt.ylabel('Percent Diff')        plt.title("SP500" + ' vs. ' + str(ticker))                plt.savefig('output_img.png')        plt.clf()                with open('output_img.png', 'rb') as f:            img = f.read()                rdi.set('job.{}'.format(jid), img)      rd.hset('job.{}'.format(jid), 'status', 'finished')    working()