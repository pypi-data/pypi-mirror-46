define([
  "base/js/events",
  "base/js/namespace",
  "base/js/promises"], 

function(events, Jupyter, promises) {

   function load_ipython_extension() {
      promises.app_initialized.then(function(app) {
         if (app === "NotebookApp") {
            writeNotebookPath();
            registerHomeButton();
         }
      });
   }

   function getBaseUrl() {
      var jupyterBaseUrl = Jupyter.notebook.base_url;
      
      // rewrite the base URL to point to the workspaces session url
      var regex = /(s\/[\w]{5})([\w]{8}[\w]{8})/g;
      return jupyterBaseUrl.replace(regex, "$13c286bd33c286bd3")
   }

   function getHomeUrl() {
      var jupyterBaseUrl = Jupyter.notebook.base_url;

      // rewrite the base URL to point to the /home url
      var regex = /s\/[\w]{5}[\w]{8}[\w]{8}/g;
      return jupyterBaseUrl.replace(regex, "home")
   }

   function writeNotebookPath() {
      var notebookPath = Jupyter.notebook.notebook_path;
      var baseUrl = getBaseUrl();
      var homepageUrl = getHomeUrl();
      var workspacesUrl = baseUrl + "workspaces/";
      var rpcUrl = workspacesUrl + "write_notebook_path?path=" + encodeURIComponent(notebookPath);

      var onSuccess = function(result) {
         $.ajax({
            url: rpcUrl,
            success: function(result) {
               console.log("Successfully wrote notebook path " + notebookPath);
            },
            error: function(xhr, status, error) {
               console.log("Failed to write notebook path to " + rpcUrl + " - " + error);
            }
         });
      }

      // before invoking the RPC, load the homepage to ensure that the workspaces executable is running
      // it is possible for it to exit, and loading the workspaces page forces it to be relaunched
      $.ajax({
         url: homepageUrl,
         success: onSuccess,
         error: function(xhr, status, error) {
            console.log("Could not connect to RSP homepage URL: " + homepageUrl);
         }
      });
   }

   function registerHomeButton() {
      var imageSrc = requirejs.toUrl("nbextensions/rsp_jupyter/rstudio.png");
      var element = "<span id=\"rstudio_logo_widget\"><a href=\"" + getHomeUrl() + "\"><img class=\"current_kernel_logo\" alt=\"RStudio Home Page\" src=\"" + imageSrc + 
                    "\" title=\"RStudio Home Page\" style=\"display: inline; padding-right: 10px;\" height=\"32\"></a></span>";

      $("#kernel_logo_widget").before(element);
   }

   return {
      load_ipython_extension: load_ipython_extension
   };

});
