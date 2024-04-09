from v0.models import Dataset
import erdantic as erd
diagram = erd.create(Dataset)
diagram.draw("spif.svg")
