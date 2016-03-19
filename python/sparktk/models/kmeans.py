from sparktk.simple import SimpleObj

class KMeansModel(SimpleObj):

    def __init__(self, context, frame, columns, scalings, k=2, maxIterations=20, epsilon=1e-4, initializationMode = "k-means||"):
        self._context = context
        self._columns = columns
        self._scalings = scalings
        _scala_obj = context.sc._jvm.org.trustedanalytics.at.model.KMeans
        c = context.jconvert.to_scala_vector_string(columns)
        s = context.jconvert.to_scala_vector_double(scalings)
        self._scala = _scala_obj.train(frame._scala, c, s, k, maxIterations, epsilon, initializationMode)

    @property
    def columns(self):
        #return list(self._scala.columns())  todo - get the from-scala to convert
        return self._columns

    @property
    def scalings(self):
        # return list(self._scala.scalings())  todo - get the from-scala to convert
        return self._scalings

    @property
    def k(self):
        return self._scala.k()

    @property
    def max_iterations(self):
        return self._scala.maxIterations()

    @property
    def initialization_mode(self):
        return self._scala.initializationMode()

    @property
    def sizes(self):
        sizes = self._context.jconvert.from_option(self._scala.sizes())
        return list(sizes) if sizes else None

    def compute_sizes(self, frame):
        self._scala.computeClusterSizes(frame._scala, self._context.jconvert.to_option(None))
        return self.sizes

    @property
    def centroids(self):
        return [list(item) for item in list(self._scala.centroids())]

    @property
    def wsse(self):
        return self._scala.wsse()

    def predict(self, frame, columns=None):
        if columns is not None:
            columns = self._context.jconvert.to_scala_vector_string(columns)
        c = self._context.jconvert.to_option(columns)
        self._scala.predict(frame._scala, c)
