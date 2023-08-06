/* example.i */
%module libcolgraph
%inline %{
    #include "Graph.h"
    #include "Vertex.h"
%}

%include "Graph.h"
%include "Vertex.h"
