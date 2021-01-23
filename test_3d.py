from skimage import data
import plotly
import plotly.express as px

img = data.cells3d()[20:]
fig = px.imshow(img, facet_col=1, animation_frame=0,
                binary_string=True, binary_format='jpg')
fig.layout.annotations[0]['text'] = 'Cell membranes'
fig.layout.annotations[1]['text'] = 'Nuclei'
plotly.io.show(fig)