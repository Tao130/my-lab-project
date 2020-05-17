from django.shortcuts import render, redirect
import pandas as pd
import os
import plotly.graph_objects as go
from plotly.offline import plot
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required
def geneidfunc(request):
    if request.method == 'POST':
        # path設定
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'gene_FPKM_tracking.tabular')

        # geneIdの入力受け取り
        geneid = request.POST['geneid']

        columns = ['K2nd_FPKM', 'K4th_FPKM', 'K6th_FPKM', 'SL2nd_FPKM', 'SL4th_FPKM', 'SL6th_FPKM']
        lines = ['Koshihikari', 'SL203×218']
        headings = ['K2nd', 'K4th', 'K6th', 'SL2nd', 'SL4th', 'SL6th']

        df = pd.read_table(path)
        df = df[df['gene_short_name']=="{}".format(geneid)]
        if df.size == 0:
            return render(request, 'error.html', {'geneid':geneid})

        df = df[columns]
    
        fpkms = []
        for column in columns:
            fpkm = round(df.iloc[0]["{}".format(column)], 2)
            fpkms.append(fpkm)

        # グラフ描画
        fig = go.Figure(data=[
            go.Bar(name='2nd leaf', x=lines, y=[fpkms[0], fpkms[3]]),
            go.Bar(name='4th leaf', x=lines, y=[fpkms[1], fpkms[4]]),
            go.Bar(name='6th leaf', x=lines, y=[fpkms[2], fpkms[5]])
            ], layout_title_text="{}".format(geneid))

        fig.update_layout(barmode='group')
        plot_fig = plot(fig, output_type='div', include_plotlyjs=False)

        return render(request, 'graph.html', {'geneid': geneid, 'fpkms': fpkms, 'graph': plot_fig, 'headings': headings})
    else: 
        return render(request, 'geneid.html')

def loginfunc(request):
    if request.method == 'POST':
        usernamePosted = request.POST['username']
        passwordPosted = request.POST['password']
        user = authenticate(request, username=usernamePosted, password=passwordPosted)
        if user is not None:
            login(request, user)
            return redirect('rnaseq')
        else:
            return render(request, 'login.html', {'error': "ユーザー名またはパスワードが間違っています"})
    else: return render(request, 'login.html')

def logoutfunc(request):
    logout(request)
    return redirect('login')