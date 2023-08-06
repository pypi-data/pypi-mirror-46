from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

def plotPieChart(positive, wpositive, spositive, negative, wnegative,snegative, neutral, searchTerm, noOfSearchTerms):
#--Create pie chart--#
    labels = ['Positive [' + str(positive) + '%]', 'Weakly Positive [' + str(wpositive) + '%]', 'Strongly Positive [' + str(spositive) + '%]', 'Neutral [' + str(neutral) + '%]',
              'Negative [' + str(negative) + '%]', 'Weakly Negative [' + str(wnegative) + '%]', 'Strongly Negative [' + str(snegative) + '%]']
    sizes = [positive, wpositive, spositive, neutral, negative, wnegative, snegative]
    colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']
    plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(labels, loc="best") #Changes to code from plt.legend(patches, labels, loc="best")
    plt.title("\nAnalyzing " + str(noOfSearchTerms) + " tweets on " + searchTerm)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def barGraphP(pos,neg,nums):
    n = 8
    X = np.arange(n)
    #pos=[]
    #neg=[]
    #for name in files:
        #pos.append(temp[0] + temp[1] + temp[2])
        #neg.append(temp[3] + temp[4] + temp[5])
        #nums.append(name + '\n' + 'with' +'\n' + str(temp[7]) + '\n' + 'tweets')    
    YP = np.array(pos)
    YN = np.array(neg)
    #plt.axes([2, 2, 0.95, 0.95]) not supported with tight layout
    plt.bar(X, +YP, facecolor='#9999ff', edgecolor='white', label='positive tweets')
    plt.bar(X, -YN, facecolor='#ff9999', edgecolor='white', label='negative tweets')
    plt.legend(loc='upper right')
    plt.ylim(-40,60)
    for x, y in zip(X, YP):
        plt.text(x , y + 0.05, '%.2f' % y + '%', ha='center', va= 'bottom')
    for x, y in zip(X, YN):
        plt.text(x , -y - 0.1, '%.2f' % y + '%', ha='center', va= 'top')
    plt.title("\nAnalyzing positive and negative tweet percentage ")
    plt.xticks(X, nums, fontsize=12)
    plt.tight_layout()
    plt.show()


def cloud(hash):  # @ReservedAssignment
#--Create word cloud--#    
    wc = WordCloud(background_color="white", relative_scaling=0.5).generate(hash)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.title('Frequent hashtags from Tweets fetched.', color='black')
    plt.show()


def plottest(Gr,nodelist,mainnode):
    nodelist=list(dict.fromkeys(nodelist))
    Gr.add_nodes_from(nodelist)
    for i in range(len(nodelist)):
        Gr.add_edge(nodelist[i],mainnode)
    return Gr


