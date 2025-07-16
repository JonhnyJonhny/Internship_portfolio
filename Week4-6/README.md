1. Helm là gì?
    
    Helm là trình quản lý gói và công cụ quản lý úng dụng cho kubernetes, đóng gói nhiều tài nguyên kubernetes vào một đơn vị triển khai logic duy nhất được gọi là charts, bên trong của charts sẽ là templates, định nghĩa tài nguyên để triển khai lên k8s.
    
2. Install guide:
    
    Target: chạy được microservice đơn giản bằng python, return tin nhắn khi được gọi, cài đặt bằng manifest sau đó refract lại bằng helm và có kết nối với database redis.
    
    Install Components:
    
    Kind
    
    curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.16.0/kind-linux-amd64
    chmod +x ./kind
    sudo mv ./kind /usr/local/bin/kind
    
    Helm
    
    ```jsx
    curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
    chmod 700 get_helm.sh
    ./get_helm.sh
    ```
    
    Docker
    
    sudo apt install -y docker.io
    
    Kubectl
    
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
    
    Tạo Directory. VD: app
    
    Tạo Kind config
    
    kind: Cluster
    apiVersion: [kind.x-k8s.io/v1alpha4](http://kind.x-k8s.io/v1alpha4)
    name: pong
    nodes:
    
    - role: control-plane
    extraPortMappings:
        - containerPort: 30001
        hostPort: 30001
        protocol: TCP
    
    sau đó chạy lệnh:
    
    Kind create cluster —config kind-config.yaml —name <tên tự chọn hoặc để trống thì default sẽ là kind>
    
    Để kiểm tra port exposed có đúng không có thể chạy lệnh:
    
    docker ps | grep 30001
    
    Sau khi đã cài xong KinD cluster, tiếp đến tạo app.py:
    
    from flask import Flask
    import redis
    import os
    
    app = Flask(**name**)
    r = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD", None),
    decode_responses=True
    )
    
    @app.route("/")
    def index():
    count = r.incr("hits")
    return f"Hello from Flask! View count: {count}"
    
    if **name** == "**main**":
    app.run(host="0.0.0.0", port=5000)
    
    Tạo thêm 1 file Requirements.txt
    
    Flask
    
    Redis
    
    Sau đó build bằng Docker và load vào KinD
    
    docker build -t python-app:latest .
    
    kind load docker-image python-app:lastest <Nếu đặt tên cho cluster thì thêm —name tên cluster hoặc không thì bỏ trống và nó sẽ mặc định sử dụng tên kind>
    
    Tiếp theo tạo Helm Chart có structure như này
    
    App/
    
    |— Chart.yaml
    
    |— values.yaml
    
    |— Templates
    
    |— deployment.yaml
    
    |— service.yaml
    
    |— _helpers.tpl 
    
    Chart.yaml
    
    apiVersion: v2
    name: python-microservice
    description: A simple Flask microservice connected to Redis
    type: application
    version: 0.1.0
    appVersion: "1.0.0"
    
    values.yaml
    
    image:
    repository: python-microservice
    tag: latest
    pullPolicy: IfNotPresent
    
    service:
    type: NodePort
    port: 80
    nodePort: 30001
    
    redisHost: redis-master
    redisPort: 6379
    redisPasswordSecretName: redis
    
    deployment.yaml
    
    apiVersion: apps/v1
    kind: Deployment
    metadata:
    name: {{ include "python-microservice.fullname" . }}
    spec:
    replicas: 1
    selector:
    matchLabels:
    app: {{ include "[python-microservice.name](http://python-microservice.name/)" . }}
    template:
    metadata:
    labels:
    app: {{ include "[python-microservice.name](http://python-microservice.name/)" . }}
    spec:
    containers:
    - name: {{ .Chart.Name }}
    image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
    ports:
    - containerPort: 5000
    env:
    - name: REDIS_HOST
    value: {{ .Values.redisHost | quote }}
    - name: REDIS_PORT
    value: "{{ .Values.redisPort }}"
    - name: REDIS_PASSWORD
    valueFrom:
    secretKeyRef:
    name: {{ .Values.redisPasswordSecretName }}
    key: redis-password
    
    service.yaml
    
    apiVersion: v1
    kind: Service
    metadata:
    name: {{ include "python-microservice.fullname" . }}
    spec:
    type: {{ .Values.service.type }}
    selector:
    app: {{ include "[python-microservice.name](http://python-microservice.name/)" . }}
    ports:
    - protocol: TCP
    port: {{ .Values.service.port }}
    targetPort: 5000
    nodePort: {{ .Values.service.nodePort }}
    
    _helpers.tpl
    
    {{/*
    Return the full name of the chart (used for naming K8s resources)
    */}}
    {{- define "python-microservice.fullname" -}}
    {{ .Release.Name }}-{{ .Chart.Name }}
    {{- end }}
    
    {{/*
    Return the name of the chart
    */}}
    {{- define "[python-microservice.name](http://python-microservice.name/)" -}}
    {{ .Chart.Name }}
    {{- end }}
    
    Trước khi deploy thì ta sẽ thêm repo của redis bằng helm qua câu lệnh
    
    helm repo add bitnami https://charts.bitnami.com/bitnami
    
    helm repo update
    
    helm install redis bitnami/redis
    
    Sau khi đã chuẩn bị xong hết file, cài đặt app bằng câu lệnh:
    
    helm install <tên tự chọn> ./<tên file chart>
    
    sau khi cài đặt thì ta có thể kiểm tra xem các pods đã chạy chưa bằng câu lệnh 
    
    kubectl get pods 
    
    và để kiểm tra xem ứng dụng có chạy đúng không thì ta sẽ kết nối với IP theo sau là port 30001 hoặc dùng câu lệnh 
    
    curl http://<ip>:30001 để check service có trả lại tin khi được gọi không
    
3. Cách setup NFS cho Redis
    
    cài đặt NFS server: sudo apt install -y nfs-kernel-server
    
    tạo file directory cho nfs:
    
    sudo mkdir -p /srv/nfs/redis
    sudo chown nobody:nogroup /srv/nfs/redis
    sudo chmod 777 /srv/nfs/redis
    
    cài đặt export file:
    
    sudo nano /etc/exports
    
    apply lệnh export:
    
    sudo exportfs -a
    
    nếu cần thì khởi động lại và kiểm tra trạng thái server:
    
    sudo systemctl enable nfs-server
    
    sudo systemctl restart nfs-server
    
    sau khi đã cài đặt xogn nfs-server thì tiếp theo tạo 2 file yaml cho pvc (Persistent volume claim) và pv (Persistent volume)
    
    nfs-pv.yaml
    
    apiVersion: v1
    kind: PersistentVolume
    metadata:
    name: redis-nfs-pv
    spec:
    capacity:
    storage: 1Gi
    accessModes:
    - ReadWriteMany
    nfs:
    server: <YOUR_NFS_SERVER_IP>
    path: /srv/nfs/redis
    persistentVolumeReclaimPolicy: Retain
    storageClassName: redis-nfs
    
    nfs-pvc.yaml
    
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
    name: redis-nfs-pvc
    spec:
    accessModes:
    - ReadWriteMany
    resources:
    requests:
    storage: 1Gi
    storageClassName: redis-nfs
    
    apply 2 file yaml bằng lệnh kubectl, sau đó tạo thêm 1 file redis-values.yaml cho helm:
    
    architecture: standalone
    master:
    persistence:
    enabled: true
    existingClaim: redis-nfs-pvc
    storageClass: ""
    
    cài lại redis và upgrade chart nếu đang chạy từ trước
    
4. CI/CD là gì?
    
    Là một tập hợp các phương pháp và công cụ giúp tự động hóa quy trình phát triển, kiểm tra và triển khai phần mềm với mục tiêu chính là đẩy nhanh tốc độ phát hành phần mềm, giảm lỗi và nâng cao tính nâng cao tính ổn định của các phiên bản phát hành.
    
    CI/CD là viết tắt của Continuous Intergration/Continuous Delivery - Development
    
    1. CI - Continuous Integration
        
        là quá trình liên tục kiểm tra và tích hợp code mới vào code chính của dự án. Mục tiêu của CI là đảm bảo rằng bất kỳ thay đổi nào trong code đều được kiểm tra ngay lập tức để tránh lỗi gây ảnh hưởng đến hệ thống. Hoạt động như một hệ thống kiểm tra tự động, mỗi khi code được thay đổi và comit lên hệ thống, các bài kiểm tra sẽ tự động chạy để đảm bảo code không bị lỗi
        
    2. CD - Continuous Delievery & Deployment
        - Continuous Delievery: đảm bảo rằng code luôn sẵn sàng để triển khai bất cứ lúc nào. Sau khi code đã qua được hết công đoạn kiểm tra CI, code sẽ được đặt ở trạng thái sẵn sàng để triển khai và việc triển khai này có thể được đặt làm thủ công
        - Continuous Deployment: tự động triển khai code sau khi nó đã vượt qua tất cả kiểm tra. Không cần sự can thiệp thủ công, hệ thống tự động đưa code vào môi trường production.
  5. Configuration
![phong](images/1.png)
![phong](images/2.png)
![phong](images/3.png)
![phong](images/4.png)
