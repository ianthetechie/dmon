<!DOCTYPE html>
<html class="no-js" lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{ page_title }}</title>
    <link rel="stylesheet" href="{{ base_url }}/css/foundation.min.css" />
    <script src="{{ base_url }}/js/vendor/modernizr.min.js"></script>
    <style type="text/css">
      div.progress {
        background-color: #999;
      }

      .label {
        margin-bottom: 0.2em;
      }
      
      .thick {
        height: 3rem;
        font-size: 2.45rem;
      }

      div.progress .meter {
        background-color: orange;
      }
      
      span.meter {
        white-space: nowrap;
        color: white;
      }

      .footer {
        text-align: center;
        color: #aaa;
        font-size: 12px;
      }
    </style>
  </head>
  <body>
    
    <div class="row">
      <div class="small-12 columns">
        <h1>{{ page_heading }}</h1>
      </div>
    </div>

    <div class="row">
      <div class="small-12 columns">
        %if page_subheading:
        <h5>{{ page_subheading }}</h5>
        %end

        <h6>Average ping to google.com</h6>
        % for timeframe in timeframes:
        <div id="{{timeframe}}-div" class="progress large-12 thick">
          <span id="{{timeframe}}-span" class="meter" style="width: 50%">Updating...</span>
        </div>
        % end

        <div class="large-12">
          % for service in services:
          <span id="{{service}}-span" class="label alert thick">{{service}}</span>
          % end
        </div>
        <hr />
      </div>
    </div>

    <div class="footer">
      Developed by Bored-H4x0rs-R-Us. Sponsored by Insomniac Productions.
    </div>
    
    <script src="{{ base_url }}/js/vendor/jquery.min.js"></script>
    <script src="{{ base_url }}/js/foundation.min.js"></script>
    <script src="{{ base_url }}/js/dmon.js"></script>
    <script>
      $(document).foundation();
      $(document).ready(function() {
        dmon.setTimeframes({{! timeframes}});
        dmon.updatePing({{! current_ping}});

        dmon.setServices({{! services}});
        dmon.updateServices({{! server_data}});
      });
    </script>
  </body>
</html>
