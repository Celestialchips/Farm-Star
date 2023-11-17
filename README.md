# project artemis

## Getting started

## making changes

```
git clone https://gitlab.com/cercleholdings/artemis.git
git checkout -b <mybranchname>
Make your changes in the code.
git add <myfiles> or git add .
git commit -m 'commit message'
git pull origin main
git push origin <mybranchname>
```
Merge Requests require approval before being commited.
Notify maintainer

## Software Architecture

```mermaid
graph LR
    subgraph Frontend
    HTML_CSS[("HTML/CSS")]
    React[("/React")]
    JS[("JavaScript")]
    end

    subgraph Backend
    Django[("/Django App")]
    Celery[("Celery for Scheduling")]
    Redis[("Redis Cache")]
    end

    subgraph Data Storage
    Cassandra[("/Cassandra DB")]
    Neo4j[("/Neo4j Graph DB")]
    end

    subgraph DevOps
    GitLab[("GitLab CI/CD")]
    Docker[("Docker Containers")]
    K8s[("Kubernetes Orchestration")]
    NGINX[("NGINX Server/Load Balancer")]
    DigitalOcean[("Digital Ocean Cloud")]
    end

    subgraph Monitoring
    ELK[("ELK Stack")]
    end

    subgraph External Services
    ArcGIS[("ArcGIS for Mapping")]
    Cloudflare[("Cloudflare CDN")]
    end

    Frontend -->|API requests| Django
    Django -->|Data Handling| Cassandra
    Django -->|Graph Queries| Neo4j
    Django -->|Task Queue| Celery
    Celery -->|Caching| Redis
    Django -->|Load Balance & Serve| NGINX
    NGINX -->|Deployed on| DigitalOcean
    Django -->|Logging| ELK
    Frontend -->|Static Content| Cloudflare
    GitLab -->|CI/CD for| Docker
    Docker -->|Managed by| K8s
    K8s -->|Runs on| DigitalOcean
    Django -->|Geospatial data| ArcGIS

```
