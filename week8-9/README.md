1. Ansible là gì?
    
    Ansible là một công cụ mã nguồn mở, cho phép tự động hóa và phối hợp đa nền tảng ở quy mô lớn, được hỗ trợ bởi redhat và một cộng đồng người dùng lớn, Ansible là một công cụ có thể cải thiện đáng kể hiệu quả và tính nhất toán của môi trường sử dụng.
    
    Các máy sử dụng Ansible sẽ được chia ra làm 2 loại, control node và managed node, control node sẽ là máy được cài Ansible, bắt buộc phải có ít nhất 1 máy làm control node và có thể có thêm backup control node. Managed node là các máy được kiểm soát bởi control node. Ansible hoạt động bằng cách kết nối với các managed node qua mạng và gửi đi một phần mềm nhỏ tên là Ansible module, sau đó Ansible sẽ kích hoạt các module này qua SSH và xóa đi sau khi đã hoàn thành nhiệm vụ. Yêu cầu duy nhất để hoạt động là phải có key để access các managed node, cơ bản nhất có thể dùng key SSH hoặc các dạng xác thực khác cũng được.
    
    Ansible sử dụng ngôn ngữ đơn giản theo dạng YAML, để định nghĩa các playbook theo định dạng dữ liệu mà người dùng có thể đọc được,dễ hiểu. Module là phẩn đảm nhiệm hoàn thành tác vụ, còn playbook sẽ là hướng dẫn để hoàn thành tác vụ, để cho máy đạt được trạng thái mong muốn được cài trong module. Người dùng có thể chọn các playbook đã được làm sẵn để dùng hoặc tự mình viết code cho playbook dựa theo yêu cầu riêng.
    
    cấu trúc file cơ bản của Ansible:
    
    các file all.yml là cho host của từng giai đoạn 
    
    ansible/
    ├── ansible.cfg                   # config Ansible
    ├── requirements.yml              
    ├── inventory/
    │   ├── dev/
    │   │   ├── hosts                # File inventory của dev
    │   │   └── group_vars/
    │   │       └── all.yml           
    │   ├── staging/
    │   │   ├── hosts                # File inventory cho staging
    │   │   └── group_vars/
    │   │       └── all.yml
    │   └── prod/
    │       ├── hosts                 # File inventory cho production
    │       └── group_vars/
    │           └── all.yml
    ├── roles/
    │   ├── common/                   
    │   │   ├── tasks/
    │   │   ├── handlers/
    │   │   ├── templates/
    │   │   ├── files/
    │   │   └── vars/
    │   ├── app/
    │   │   ├── tasks/
    │   │   ├── templates/
    │   │   ├── files/
    │   │   └── vars/
    │   └── redis/
    │       ├── tasks/
    │       ├── templates/
    │       ├── files/
    │       └── vars/
    ├── playbooks/   # Playbook để deploy application
    │   ├── site.yml                  
    │   ├── deploy_app.yml
    │   └── deploy_redis.yml
    ├── files/                        
    └── templates/
    

Ansible Galaxy: là một repo để người dùng chia sẻ các role mình đã tạo cho Ansible, cho phép người dùng khác tải về và sử dụng, giúp giảm thời gian setup Ansible bằng cách sử dụng các roles và collection có sẵn, đồng thời giúp tăng sự hợp tác và chia sẻ kiến thức
