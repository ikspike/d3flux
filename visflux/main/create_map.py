from cobra.flux_analysis import pfba
import itertools
import cobra
import sys


import visflux as d3f
from visflux.core.flux_layouts import render_model
from visflux import flux_map

from jinja2 import Template


custom_css = \
    """
{% for item in items %}
text#{{ item }} {
    font-weight: 900;
}
{% endfor %}
text.cofactor {
    fill: #778899;
}
"""

css = Template(custom_css).render(
    items=['succ_c', 'ac_c', 'etoh_c', 'for_c', 'co2_c', 'lac__D_c'])

if (len(sys.argv) == 1):
    raise RuntimeError('JSON file name not provided.')
model_name = sys.argv[1]
name_stem = model_name.rsplit('.', 1)[0].rsplit('/', 1)[0]
model = cobra.io.load_json_model(model_name)

# model.add_reaction(ecoli.reactions.ALDD2x)
# d3f.update_cofactors(model, ['nadh_c'])


#model.reactions.EX_glc_e.lower_bound = -1
#model.reactions.EX_xyl_e.lower_bound = -6


for obj in itertools.chain(model.reactions, model.metabolites):
    try:
        del obj.notes['map_info']['flux']
        # Initialize empty map_info field in object notes
        if 'map_info' not in obj.notes:
            obj.notes['map_info'] = {}
    except KeyError:
        pass


# model.reactions.PPCK.notes['map_info']['group'] = 2
# model.reactions.MDH.notes['map_info']['group'] = 2
# model.reactions.FUM.notes['map_info']['group'] = 2

# model.reactions.PFL.notes['map_info']['group'] = 'ko'
# model.reactions.ACKr.notes['map_info']['group'] = 'ko'

# Just a single example, but many metabolite names could be better aligned
# model.metabolites.get_by_id('f6p_c').notes['map_info']['align'] = 'center left'

# test
pfba(model)





# Output html file
html = flux_map(model, figsize=(1280, 1024), inactive_alpha=0.5,
                flux_dict={rxn.id: None for rxn in model.reactions})
with open('./' + name_stem + '.html', 'w') as f:
    f.write('<!DOCTYPE html> <html> <head>' +
            '<title>' + name_stem + '</title>\n \
        <script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.3.2/require.min.js" defer async="true" integrity="sha256-Vjusm6Kh2U7/tb6jBh+MOfxnaf2TWsTph34bMKhC1Qc=" crossorigin="anonymous"></script>\n \
        <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.5.1/jquery.min.js" integrity="sha512-bLT0Qm9VnAYZDflyKcBaQ2gg0hSYNQrJ8RilYldYQ1FxQYoCLtUjuuRuZo+fjqhx/qtq/1itJ0C2ejDxltZVFg==" crossorigin="anonymous"></script>\n \
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/js/bootstrap.min.js" defer async="true" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>\n \
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">\n \
        </head> <body>')
    f.write(html.data)
    f.write('</body> </html>')
