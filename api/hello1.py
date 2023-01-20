from flask import Flask, request, jsonify
from flask_cors import CORS
import  matplotlib.pyplot as plt
import numpy as np
import base64
from io import BytesIO

app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    return "<p> Welcome PriServer!</p>"

@app.route("/test", methods=['POST'])
def test():
    json = request.get_json()

    name = json['name']
    value = json['price']

    books = {'name':name, 'value':value}

    return jsonify(books)

@app.route("/print", methods=['POST'])
def write():
    json = request.get_json()

    x = json['x']
    y = json['y']

    x = np.array(x, dtype=np.uint8)
    y = np.array(y, dtype=np.uint8)

    plt.plot(x, y)

    ofs = BytesIO()
    plt.savefig(ofs, format="jpg")
    png_data = ofs.getvalue()
    plt.close()

    base64_data = base64.b64encode(png_data).decode()

    data = {"value":base64_data}

    return jsonify(data)

def throw_error_json():
    return {"value":None}

class GraphPloter:
    def __init__(self,json):
        self.json = json
        self.graph_type = json["datasets"][0]["type"]
        self.response = None
        self.datasets = json["datasets"]
    
    # def judge_line(self):
    #     xdata = self.json["xdata"]
    #     for dataset in self.json["datasets"]:
    #         if len(dataset["ydata"]) != xdata:#要素の長さを見る
    #             return False
    #         for y in dataset["ydata"]:
    #             if type(y) == "":
    #     return True

    def getMarker(self, marker):
        maerkers = {"point":".", "circle":"o", "rect":"s", "star":"*", "crossRot":"x", "cross":"+"}
        # if(marker=="circle"):
        #     return "."
        return maerkers[marker]


    def plot(self):
        if self.graph_type == "line":              
            for dataset in self.datasets:
                print(self.datasets)
                print(dataset["ydata"])
                print(dataset["pointStyle"])
                plt.plot(self.json["xdata"],dataset["ydata"], color=dataset["color"],linestyle=dataset["linestyle"], marker=self.getMarker(dataset["pointStyle"]), markersize=dataset["pointRadius"], label=dataset["legend"]) 
                if(dataset["legend"] != ""):
                    plt.legend()      
                
            if(self.json["grid"]):
                plt.grid()

            if(self.json["title"]!=""):
                plt.title(self.json["title"])

            if("xLabel" in self.json):
                plt.xlabel(self.json["xLabel"])

            if("yLabel" in self.json):
                plt.ylabel(self.json["yLabel"])


        elif self.graph_type == "bar":
            margin = 0.2
            totoal_width = 1 - margin 
            width = totoal_width/len(self.datasets)
            sum_ydata = [0]*len(self.json["xdata"])
            print(sum_ydata)
            for index, dataset in enumerate(self.datasets):
                ydata = dataset["ydata"]
                ydata = [int(i) for i in ydata]
                pos =[ int(i+1) - totoal_width *( 1- (2*index+1)/len(self.datasets) )/2 for i,x in enumerate(self.json["xdata"]) ]
                if("barh" in self.json and self.json["barh"]):
                    if("stacked" in self.json and self.json["stacked"]):
                        if(index == 0):
                            plt.barh(self.json["xdata"], ydata, color=dataset["color"], align="center")
                        else:
                            pre_ydata = self.datasets[index-1]["ydata"]
                            pre_ydata = [int(i) for i in pre_ydata]
                            sum_ydata = [sum_ydata[i]+pre_ydata[i] for i in range(len(sum_ydata))]
                            plt.barh(self.json["xdata"], ydata, color=dataset["color"], align="center", left=sum_ydata)
                    else:
                        plt.barh(pos, ydata, color=dataset["color"], align="center", width=width)
                else:
                    if("stacked" in self.json and self.json["stacked"]):
                        if(index == 0):
                            plt.bar(self.json["xdata"], ydata, color=dataset["color"], align="center")
                        else:
                            pre_ydata = self.datasets[index-1]["ydata"]
                            pre_ydata = [int(i) for i in pre_ydata]
                            sum_ydata = [sum_ydata[i]+pre_ydata[i] for i in range(len(sum_ydata))]
                            print(pre_ydata)
                            plt.bar(self.json["xdata"], ydata, color=dataset["color"], align="center", bottom=sum_ydata)
                    else:
                        plt.bar(pos, ydata, color=dataset["color"], align="center", width=width)

            
            if(self.json["grid"]):
                plt.grid()

            if(self.json["title"]!=""):
                plt.title(self.json["title"])

            if("xLabel" in self.json):
                plt.xlabel(self.json["xLabel"])

            if("yLabel" in self.json):
                plt.ylabel(self.json["yLabel"])


        elif self.graph_type == "scatter":
            for dataset in self.datasets:
                xdata = dataset["xdata"]
                ydata = dataset["ydata"]
                c = dataset["color"]
                marker=self.getMarker(dataset["pointStyle"])
                markersize=dataset["pointRadius"]
                markersize = int(markersize)*10
                plt.scatter(xdata,ydata,c=c,marker=marker, s=markersize)
                if(self.json["grid"]):
                    plt.grid()

                if(self.json["title"]!=""):
                    plt.title(self.json["title"])

                if("xLabel" in self.json):
                    plt.xlabel(self.json["xLabel"])

                if("yLabel" in self.json):
                    plt.ylabel(self.json["yLabel"])


        elif self.graph_type == "bubble":
            for dataset in self.datasets:
                xdata = dataset["xdata"]
                ydata = dataset["ydata"]
                rdata = dataset["rdata"]
                rdata = [int(i) for i in rdata]
                c = dataset["color"]                
                marker=self.getMarker(dataset["pointStyle"])
                plt.scatter(xdata,ydata,c=c,marker=marker,s=rdata)
                if(self.json["grid"]):
                    plt.grid()

                if(self.json["title"]!=""):
                    plt.title(self.json["title"])

                if("xLabel" in self.json):
                    plt.xlabel(self.json["xLabel"])

                if("yLabel" in self.json):
                    plt.ylabel(self.json["yLabel"])

        elif self.graph_type == "pie":
            labels = self.json["labels"]
            for dataset in self.datasets:
                data = dataset["data"]
                colors=dataset["colors"]
                plt.pie(data,labels=labels,colors=colors)   

            if(self.json["title"]!=""):
                    plt.title(self.json["title"])
        
        elif self.graph_type == "doughnut":
            labels = self.json["labels"]
            for dataset in self.datasets:
                data = dataset["data"]
                colors=dataset["colors"]    
                plt.pie(data,labels=labels,colors=colors)   
            centre_circle = plt.Circle((0,0),0.6,color='black', fc='white',linewidth=1.25)
            fig = plt.gcf()
            fig.gca().add_artist(centre_circle)

            if(self.json["title"]!=""):
                    plt.title(self.json["title"])
        # elif self.graph_type == "polarArea":
        # elif self.graph_type == "radar":
        else:
            plt.text(0.5,0.5,"sorry sorry")

    # def get_response():
    #     self.judge()
    #     return self.response



@app.route("/graph", methods=['POST'])
def graph():
    json = request.get_json()
    graphPloter = GraphPloter(json)
    graphPloter.plot()

    ofs = BytesIO()
    plt.savefig(ofs, format="jpg")
    png_data = ofs.getvalue()
    plt.close()

    base64_data = base64.b64encode(png_data).decode()

    data = {"value":base64_data}

    return jsonify(data)