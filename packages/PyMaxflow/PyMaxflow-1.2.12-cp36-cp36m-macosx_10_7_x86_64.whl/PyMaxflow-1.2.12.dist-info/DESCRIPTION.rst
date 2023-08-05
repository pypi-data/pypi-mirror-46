
PyMaxflow is a Python library for graph construction and
maxflow computation (commonly known as `graph cuts`). The
core of this library is the C++ implementation by
Vladimir Kolmogorov, which can be downloaded from his
`homepage <http://www.cs.ucl.ac.uk/staff/V.Kolmogorov/>`_.
Besides the wrapper to the C++ library, PyMaxflow offers

* NumPy integration,
* methods for the construction of common graph
  layouts in computer vision and graphics,
* implementation of algorithms for fast energy
  minimization which use the `maxflow` method:
  the alpha-beta-swap and the alpha-expansion.



