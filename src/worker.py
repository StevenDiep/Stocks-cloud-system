from jobs import q, update_job_status, return_job, rd, rdiimport matplotlib.pyplot as pltimport jsonfrom funcs import string_to_date_arr@q.workerdef working(jid):    update_job_status(jid, "In Progress")    data = return_job(jid)        graph_data = json.loads(rd.get("Stocks"))[data['ticker']]    x_values = string_to_date_arr(graph_data.keys())    y_values = graph_data.values()        plt.plot(x_values, y_values)    plt.savefig('output_img.png')            #encoding="utf8", errors='ignore'    with open('output_img.png', 'rb') as f:        img = f.read()    rdi.set('job.{}'.format(jid), img)    rd.hset('job.{}'.format(jid), 'status', 'finished')    working()