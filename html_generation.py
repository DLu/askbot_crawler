from collections import OrderedDict, defaultdict
import json

JQUERY_LINKS = """
<script src="http://code.jquery.com/jquery-1.11.1.min.js"></script>
<script src="http://cdn.datatables.net/1.10.4/js/jquery.dataTables.min.js"></script>
<link href="http://cdn.datatables.net/1.10.4/css/jquery.dataTables.css" rel="stylesheet" type="text/css"/>
"""

INFINITY_SORT = """
<script>
$.fn.dataTable.ext.type.order['infinity-pre'] = function ( d ) {
    if(isNaN(d)){
         return 10000;
     }
    return parseInt(d);
};
</script>
"""

def generate_table(M, id="rostable", params={}):
    if len(M)==0:
        return ''
    s = '<table class="display" id="%s">\n'%id
    s += '<thead>\n<tr><th>'
    s += '<th>'.join(M[0].keys())
    s += '\n</thead>\n<tbody>\n'
    for m in M:
        s += '<tr>'
        for k,v in m.iteritems():
            s += '<td>' + str(v)
        s += '\n'
    s += '</tbody>\n</table>\n'
    
    s += """
<script>
    $(document).ready(function() {
        $('#%s').DataTable(%s);
    } );
</script>"""%(id, json.dumps(params))
    return s
    
