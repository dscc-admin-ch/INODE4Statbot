# {{/*
# Expand the name of the chart.
# */}}
# {{- define "statbot.name" -}}
# {{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
# {{- end }}

# {{/*
# Create a default fully qualified app name.
# We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
# If release name contains chart name it will be used as a full name.
# */}}
# {{- define "statbot.fullname" -}}
# {{- if .Values.fullnameOverride }}
# {{- printf "%s" .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
# {{- else }}
# {{- $name := default .Chart.Name .Values.nameOverride }}
# {{- if contains $name .Release.Name }}
# {{- .Release.Name | trunc 63 | trimSuffix "-" }}
# {{- else }}
# {{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
# {{- end }}
# {{- end }}
# {{- end }}

# {{/*
# Common labels
# */}}
# {{- define "statbot.labels" -}}
# helm.sh/chart: {{ include "statbot.chart" . }}
# {{ include "statbot.selectorLabels" . }}
# {{- if .Chart.AppVersion }}
# app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
# {{- end }}
# app.kubernetes.io/managed-by: {{ .Release.Service }}
# {{- end }}

# {{/*
# Selector labels
# */}}
# {{- define "statbot.selectorLabels" -}}
# app.kubernetes.io/name: {{ include "statbot.name" . }}
# app.kubernetes.io/instance: {{ .Release.Name }}
# {{- end }}

# {{/*
# Create chart name and version as used by the chart label.
# */}}
# {{- define "statbot.chart" -}}
# {{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
# {{- end }}