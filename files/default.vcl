vcl 4.0;

import std;
import bodyaccess;

backend default {
  .host = "api";
  .port = "8080";
}

sub vcl_backend_response {
    set beresp.ttl = 1w;
}

sub vcl_recv {
  unset req.http.cookie;
  return (hash);
}
