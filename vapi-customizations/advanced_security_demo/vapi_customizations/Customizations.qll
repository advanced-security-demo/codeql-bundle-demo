import python
private import semmle.python.ApiGraphs
private import semmle.python.dataflow.new.RemoteFlowSources
private import semmle.python.frameworks.internal.InstanceTaintStepsHelper

module Connexion {
  API::Node request() { result = API::moduleImport("connexion").getMember("request") }

  private class ConnexionRequestSource extends RemoteFlowSource::Range {
    ConnexionRequestSource() {
      this = request().getAUse() and
      not any(Import imp).contains(this.asExpr()) and
      not exists(ControlFlowNode def | this.asVar().getSourceVariable().hasDefiningNode(def) |
        any(Import imp).contains(def.getNode())
      )
    }

    override string getSourceType() { result = "connexion.request" }
  }

  private class InstanceTaintSteps extends InstanceTaintStepsHelper {
    InstanceTaintSteps() { this = "connexion.Request" }

    override DataFlow::Node getInstance() { result = request().getAUse() }

    override string getAttributeName() {
      result in [
          // str
          "path", "full_path", "base_url", "url", "access_control_request_method",
          "content_encoding", "content_md5", "content_type", "data", "method", "mimetype", "origin",
          "query_string", "referrer", "remote_addr", "remote_user", "user_agent",
          // dict
          "environ", "cookies", "mimetype_params", "view_args",
          // json
          "json",
          // List[str]
          "access_route",
          // file-like
          "stream", "input_stream",
          // MultiDict[str, str]
          // https://werkzeug.palletsprojects.com/en/1.0.x/datastructures/#werkzeug.datastructures.MultiDict
          "args", "values", "form",
          // MultiDict[str, FileStorage]
          // https://werkzeug.palletsprojects.com/en/1.0.x/datastructures/#werkzeug.datastructures.FileStorage
          // TODO: FileStorage needs extra taint steps
          "files",
          // https://werkzeug.palletsprojects.com/en/1.0.x/datastructures/#werkzeug.datastructures.HeaderSet
          "access_control_request_headers", "pragma",
          // https://werkzeug.palletsprojects.com/en/1.0.x/datastructures/#werkzeug.datastructures.Accept
          // TODO: Kinda badly modeled for now -- has type List[Tuple[value, quality]], and some extra methods
          "accept_charsets", "accept_encodings", "accept_languages", "accept_mimetypes",
          // https://werkzeug.palletsprojects.com/en/1.0.x/datastructures/#werkzeug.datastructures.Authorization
          // TODO: dict subclass with extra attributes like `username` and `password`
          "authorization",
          // https://werkzeug.palletsprojects.com/en/1.0.x/datastructures/#werkzeug.datastructures.RequestCacheControl
          // TODO: has attributes like `no_cache`, and `to_header` method (actually, many of these models do)
          "cache_control",
          // https://werkzeug.palletsprojects.com/en/1.0.x/datastructures/#werkzeug.datastructures.Headers
          // TODO: dict-like with wsgiref.headers.Header compatibility methods
          "headers"
        ]
    }

    override string getMethodName() { result in ["get_data", "get_json"] }

    override string getAsyncMethodName() { none() }
  }
}
