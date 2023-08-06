from utils import *
from movie import movie
from plot import plot
from plot_keywords import plot_keywords
from company import company
from parental_guide import parental_guide
from technical_spec import technical_spec
from release_info import release_info
from taglines import taglines
from cast_and_crew import cast_and_crew

# main class which passes the titleid to each indiviual class
class imdb:
    def __init__(self, titleid):
        start_time = datetime.now()
        movie.__init__(self, titleid)
        plot.__init__(self, titleid)
        plot_keywords.__init__(self, titleid)
        parental_guide.__init__(self, titleid)
        company.__init__(self, titleid)
        technical_spec.__init__(self, titleid)
        release_info.__init__(self, titleid)
        taglines.__init__(self, titleid)
        cast_and_crew.__init__(self, titleid)

        time_delta = datetime.now() - start_time
        sys.stdout.write('\r' + str("Calculating time taken for data extraction") + ":  " + str(time_delta.seconds) +  "  seconds" +  '\r')
        sys.stdout.flush()
