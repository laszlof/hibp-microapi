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
  unset req.http.X-Body-Len;
  unset req.http.cookie;
  set req.http.X-Body-Len = bodyaccess.len_req_body();
  return (hash);
}

sub vcl_hash {
  # To cache POST and PUT requests
  if (req.http.X-Body-Len) {
    bodyaccess.hash_req_body();
  } else {
    hash_data("");
  }
}

sub vcl_backend_fetch {
  if (bereq.http.X-Body-Len) {
    set bereq.method = "POST";
  }
}
