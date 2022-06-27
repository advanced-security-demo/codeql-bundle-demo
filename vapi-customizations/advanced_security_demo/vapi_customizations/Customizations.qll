import python
private import semmle.python.ApiGraphs
private import semmle.python.dataflow.new.RemoteFlowSources

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
}
