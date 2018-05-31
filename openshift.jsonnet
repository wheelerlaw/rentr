local appName = "renty";
local projectName = "renty"; 

local pythonVersion = "3.6";

[
  {
    kind: "BuildConfig",
    apiVersion: "v1",
    metadata: {
      name: appName,
      annotations: {
        description: "Defines how to build the application",
        "template.alpha.openshift.io/wait-for-ready": "true"
      }
    },
    spec: {
      source: {
        type: "Git",
        git: {
          uri: "https://github.com/wheelerlaw/renty.git",
          // ref: "master"
        },
        contextDir: "${CONTEXT_DIR}"
      },
      strategy: {
        type: "Source",
        sourceStrategy: {
          from: {
            kind: "ImageStreamTag",
            namespace: "openshift",
            name: "python:" + pythonVersion,
          },
          // env: [
          //   {
          //       name: "PIP_INDEX_URL",
          //       value: "${PIP_INDEX_URL}"
          //   }
          // ]
        }
      },
      output: {
        to: {
          kind: "ImageStreamTag",
          name: appName + ":latest"
        }
      },
      triggers: [
        {
          type: "ImageChange"
        },
        {
          type: "ConfigChange"
        },
        {
          type: "GitHub",
          github: {
            secret: "sosecret"
          }
        }
      ],
      postCommit: {
        script: "./manage.py test"
      }
    }
  }
]