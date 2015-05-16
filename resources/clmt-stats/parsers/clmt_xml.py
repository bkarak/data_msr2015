from xml.dom import minidom


def convert_clmtx_to_clmt_json(filename):
    result_list = []

    fp = open(filename, "r")
    doc = minidom.parse(fp)
    fp.close()

    res = doc.getElementsByTagName('result')

    for r in res:
        result_ref = {'measurement': []}

        for c in r.childNodes:
            if c.nodeName == 'id':
                result_ref['id'] = getText(c).strip()
                continue
            elif c.nodeName == 'filename':
                result_ref['filename'] = getText(c).strip()
                continue
            elif c.nodeName == 'category':
                result_ref['category'] = getText(c).strip()
                continue
            elif c.nodeName == 'measurement':
                meas_ref = {}
                result_ref['measurement'].append(meas_ref)

                for m in c.childNodes:
                    if m.nodeName == 'name':
                        meas_ref['name'] = getText(m).strip()
                        continue
                    if m.nodeName == 'value':
                        meas_ref['value'] = getText(m).strip()
                        continue
                    if m.nodeName == 'result-type':
                        meas_ref['result_type'] = getText(m).strip()
                        continue

        result_list.append(result_ref)

    return result_list


def getText(nodelist):
    rc = ""
    for node in nodelist.childNodes:
        if node.nodeType == node.TEXT_NODE:
            rc = rc + node.data

    return rc

