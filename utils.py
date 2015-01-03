def generate_table(M):
    s = '<table class="sortable">\n'
    s += '<tr><th>'
    s += '<th>'.join(M[0].keys())
    s += '\n'
    for m in M:
        s += '<tr>'
        for k,v in m.iteritems():
            s += '<td>' + str(v)
        s += '\n'
    s += '</table>\n'
    return s
    
def generate_table_page(M, preamble=''):
    s = '<script src="sorttable.js"></script>\n'
    s += preamble
    s += generate_table(M)
    return s
    
def bar_images(amount, fn1='bar.png', amount2=0, fn2='barb.png'):
    S = '<img src="%s" width="%dpx" height="16px"/>'
    s = S % (fn1, amount)
    if amount2 > 0:
        s += S % (fn2, amount2)
    return s