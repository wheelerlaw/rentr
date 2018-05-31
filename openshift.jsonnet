local appName = "renty";
local projectName = "renty"; 

local pythonVersion = "3.6";

[
  {
    kind: "ImageStream",
    apiVersion: "v1",
    metadata: {
      name: appName,
      annotations: {
        description: "Keeps track of changes in the application image"
      }
    }
  },
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
        }
      },
      strategy: {
        type: "Source",
        sourceStrategy: {
          from: {
            kind: "ImageStreamTag",
            namespace: "openshift",
            name: "python:" + pythonVersion,
          },
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