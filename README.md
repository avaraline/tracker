# Avara Tracker

## Kubernetes Installation

```
kubectl apply -f https://raw.githubusercontent.com/avaraline/tracker/main/tracker.yaml
```

### Example Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tracker
  annotations:
    ingress.kubernetes.io/ssl-redirect: "false"
spec:
  rules:
    - host: tracker.localdev.me
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: tracker
                port:
                  number: 80
```
