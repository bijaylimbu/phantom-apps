phjamf/__pycache__/                                                                                 000755  000765  000024  00000000000 13647126433 015203  5                                                                                                    ustar 00smasud                          staff                           000000  000000                                                                                                                                                                         phjamf/__pycache__/jamf_connector.cpython-37.pyc                                                    000640  000765  000024  00000016176 13647126433 022630  0                                                                                                    ustar 00smasud                          staff                           000000  000000                                                                                                                                                                         B
    ��^�4  �               @   s�   d dl mZmZ d dlmZ d dlmZ d dlm	Z	 d dl
Z
d dlZd dlmZ G dd� de�ZG dd	� d	e�Zd
d� Zedkr�e�  dS )�    )�print_function�unicode_literalsN)�BaseConnector)�ActionResult)�BeautifulSoupc               @   s   e Zd Zddd�ZdS )�RetValNc             C   s   t �t||f�S )N)�tuple�__new__r   )�clsZval1Zval2� r   �*/Users/smasud/Ian/phjamf/jamf_connector.pyr	      s    zRetVal.__new__)N)�__name__�
__module__�__qualname__r	   r   r   r   r   r      s   r   c                   sn   e Zd Z� fdd�Zdd� Zdd� Zdd� Zd	d
� Zddd�Zdd� Z	dd� Z
dd� Zdd� Zdd� Z�  ZS )�JamfConnectorc                s&   t t| ���  d | _| �� }d | _d S )N)�superr   �__init__�_state�
get_config�	_base_url)�self�config)�	__class__r   r   r      s    zJamfConnector.__init__c             C   s*   |j dkrttji �S t|�tjd�d �S )N��   z/Empty response and no information in the header)�status_coder   �phantom�APP_SUCCESS�
set_status�	APP_ERROR)r   �response�action_resultr   r   r   �_process_empty_response-   s    
z%JamfConnector._process_empty_responsec             C   s�   |j }|dkrttj|j�S y8t|jd�}|j}|�d�}dd� |D �}d�|�}W n   d}Y nX d�||�}|�	dd	��	d
d�}t|�
tj|�d �S )Nr   zhtml.parser�
c             S   s   g | ]}|� � r|� � �qS r   )�strip)�.0�xr   r   r   �
<listcomp>C   s    z8JamfConnector._process_html_response.<locals>.<listcomp>zCannot parse error detailsz(Status Code: {0}. Data from server:
{1}
�{z{{�}z}})r   r   r   r   �textr   �split�join�format�replacer   r   )r   r   r    r   ZsoupZ
error_textZsplit_lines�messager   r   r   �_process_html_response7   s    

z$JamfConnector._process_html_responsec             C   s�   y|� � }W n< tk
rH } zt|�tjd�t|���d �S d }~X Y nX d|j  kr`dk rpn nttj	|�S d�|j|j
�dd��dd��}t|�tj|�d �S )	Nz)Unable to parse JSON response. Error: {0}r   i�  z9Error from server. Status Code: {0} Data from server: {1}r'   z{{r(   z}})�json�	Exceptionr   r   r   r   r,   �strr   r   r)   r-   )r   �rr    �	resp_json�er.   r   r   r   �_process_json_responseM   s    z$JamfConnector._process_json_responsec             C   s�   t |d�r:|�d|ji� |�d|ji� |�d|ji� d|j�dd�krX| �||�S d|j�dd�krv| �||�S |js�| �||�S d	�	|j|j�
d
d��
dd��}t|�tj|�d �S )N�add_debug_dataZr_status_codeZr_textZ	r_headersztext/plain;charset=UTF-8zContent-Type� ZhtmlzJCan't process response from server. Status Code: {0} Data from server: {1}r'   z{{r(   z}})�hasattrr7   r   r)   �headers�getr6   r/   r!   r,   r-   r   r   r   r   )r   r3   r    r.   r   r   r   �_process_responsed   s    
zJamfConnector._process_responser;   c             K   s�   | � � }d }ddd�}ytt|�}W n* tk
rN   t|�tjd�|��|�S X | j	| }	y"||	f||�
dd�d�|��}
W n< tk
r� } zt|�tjd�t|���|�S d }~X Y nX | �|
|�S )Nzapplication/json)ZacceptzContent-TypezInvalid method: {0}�verify_server_certF)r:   �verifyz(Error Connecting to server. Details: {0})r   �getattr�requests�AttributeErrorr   r   r   r   r,   r   r;   r1   r2   r<   )r   Zendpointr    �method�kwargsr   r4   r:   Zrequest_funcZurlr3   r5   r   r   r   �_make_rest_call�   s.    
zJamfConnector._make_rest_callc             C   sj   | � tt|���}| �d�| j�� | jd|d d�\}}t�|�rT| �d� |�	� S | �d� |�
tj�S )NzConnecting to endpoint {}z	/accounts)ZparamszTest Connectivity Failed.zTest Connectivity PassedzAction not yet implemented)�add_action_resultr   �dict�save_progressr,   r   rD   r   �is_failZ
get_statusr   r   r   )r   �paramr    �ret_valr   r   r   r   �_handle_test_connectivity�   s    


z'JamfConnector._handle_test_connectivityc             C   st   | � d�| �� �� | �tt|���}|�d�}|�d�}| �d|�\}}t�	|�rT|�
|� |�i �}|�tj�S )NzIn action handler for: {0}�id�usernamez/computermanagement/id/40zAction not yet implemented)rG   r,   �get_action_identifierrE   r   rF   r;   rD   r   rH   Zadd_dataZupdate_summaryr   r   r   )r   rI   r    rL   rM   rJ   r   Zsummaryr   r   r   �_handle_get_system_info�   s    



	

z%JamfConnector._handle_get_system_infoc             C   sH   t j}| �� }| �d| �� � |dkr2| �|�}n|dkrD| �|�}|S )N�	action_idZtest_connectivity�get_system_info)r   r   rN   Zdebug_printrK   rO   )r   rI   rJ   rP   r   r   r   �handle_action�   s    
zJamfConnector.handle_actionc             C   s"   | � � | _| �� }|d | _tjS )N�base_url)Z
load_stater   r   r   r   r   )r   r   r   r   r   �
initialize  s    

zJamfConnector.initializec             C   s   | � | j� tjS )N)Z
save_stater   r   r   )r   r   r   r   �finalize%  s    zJamfConnector.finalize)r;   )r   r   r   r   r!   r/   r6   r<   rD   rK   rO   rR   rT   rU   �__classcell__r   r   )r   r   r      s   

&9r   c           
   C   s   dd l } dd l}| ��  |�� }|jddd� |jddddd	� |jd
dddd	� |�� }d }|j}|j}|d k	r�|d kr�dd l}|�d�}|�rb|�rby�t	�
� d }td� tj|dd�}	|	jd }
t� }||d< ||d< |
|d< t� }d|
 |d< ||d< td� tj|d||d�}|jd }W n< tk
�r` } ztdt|� � td� W d d }~X Y nX t|j���}|�� }t�|�}ttj|dd�� t	� }d|_|d k	�r�||d< |�|
|d � |�t�|�d �}ttjt�|�dd�� W d Q R X td� d S )Nr   �input_test_jsonzInput Test JSON file)�helpz-uz
--usernamerM   F)rX   Zrequiredz-pz
--password�passwordz
Password: z/loginzAccessing the Login page)r>   �	csrftokenZcsrfmiddlewaretokenz
csrftoken=ZCookieZRefererz+Logging into Platform to get the session id)r>   �datar:   Z	sessionidz3Unable to get session id from the platform. Error: �   �   )ZindentTZuser_session_token)�pudb�argparseZ	set_traceZArgumentParserZadd_argumentZ
parse_argsrM   rY   �getpassr   Z_get_phantom_base_url�printr@   r;   ZcookiesrF   Zpostr1   r2   �exit�openrW   �readr0   �loads�dumpsZprint_progress_messageZ_set_csrf_infoZ_handle_action)r^   r_   Z	argparser�argsZ
session_idrM   rY   r`   Z	login_urlr3   rZ   r[   r:   Zr2r5   �fZin_jsonZ	connectorrJ   r   r   r   �main+  sZ    



"ri   �__main__)Z
__future__r   r   Zphantom.appZappr   Zphantom.base_connectorr   Zphantom.action_resultr   r@   r0   Zbs4r   r   r   r   ri   r   r   r   r   r   �<module>   s     B                                                                                                                                                                                                                                                                                                                                                                                                  phjamf/__pycache__/jamf_connector.cpython-36.pyc                                                    000640  000765  000024  00000016065 13646101332 022612  0                                                                                                    ustar 00smasud                          staff                           000000  000000                                                                                                                                                                         3
�r�^�3  �               @   s�   d dl mZmZ d dljZd dlmZ d dlm	Z	 d dl
Z
d dlZd dlmZ G dd� de�ZG dd	� d	e�Zd
d� Zedkr�e�  dS )�    )�print_function�unicode_literalsN)�BaseConnector)�ActionResult)�BeautifulSoupc               @   s   e Zd Zddd�ZdS )�RetValNc             C   s   t jt||f�S )N)�tuple�__new__r   )�clsZval1Zval2� r   �./jamf_connector.pyr	      s    zRetVal.__new__)N)�__name__�
__module__�__qualname__r	   r   r   r   r   r      s   r   c                   sn   e Zd Z� fdd�Zdd� Zdd� Zdd� Zd	d
� Zddd�Zdd� Z	dd� Z
dd� Zdd� Zdd� Z�  ZS )�JamfConnectorc                s&   t t| �j�  d | _| j� }d | _d S )N)�superr   �__init__�_state�
get_config�	_base_url)�self�config)�	__class__r   r   r      s    zJamfConnector.__init__c             C   s*   |j dkrttji �S t|jtjd�d �S )N��   z/Empty response and no information in the header)�status_coder   �phantom�APP_SUCCESS�
set_status�	APP_ERROR)r   �response�action_resultr   r   r   �_process_empty_response-   s    
z%JamfConnector._process_empty_responsec          
   C   s�   |j }|dkrttj|j�S y8t|jd�}|j}|jd�}dd� |D �}dj|�}W n   d}Y nX dj||�}|j	dd	�j	d
d�}t|j
tj|�d �S )Nr   zhtml.parser�
c             S   s   g | ]}|j � r|j � �qS r   )�strip)�.0�xr   r   r   �
<listcomp>C   s    z8JamfConnector._process_html_response.<locals>.<listcomp>zCannot parse error detailsz(Status Code: {0}. Data from server:
{1}
�{z{{�}z}})r   r   r   r   �textr   �split�join�format�replacer   r   )r   r   r    r   ZsoupZ
error_textZsplit_lines�messager   r   r   �_process_html_response7   s    

z$JamfConnector._process_html_responsec             C   s�   y|j � }W n: tk
rF } zt|jtjdjt|���d �S d }~X nX d|j  ko\dk n  rnttj	|�S dj|j|j
jdd�jdd��}t|jtj|�d �S )	Nz)Unable to parse JSON response. Error: {0}r   i�  z9Error from server. Status Code: {0} Data from server: {1}r'   z{{r(   z}})�json�	Exceptionr   r   r   r   r,   �strr   r   r)   r-   )r   �rr    �	resp_json�er.   r   r   r   �_process_json_responseM   s    z$JamfConnector._process_json_responsec             C   s�   t |d�r:|jd|ji� |jd|ji� |jd|ji� d|jjdd�krX| j||�S d|jjdd�krv| j||�S |js�| j||�S d	j	|j|jj
d
d�j
dd��}t|jtj|�d �S )N�add_debug_dataZr_status_codeZr_textZ	r_headersr0   zContent-Type� ZhtmlzJCan't process response from server. Status Code: {0} Data from server: {1}r'   z{{r(   z}})�hasattrr7   r   r)   �headers�getr6   r/   r!   r,   r-   r   r   r   r   )r   r3   r    r.   r   r   r   �_process_responsed   s    
zJamfConnector._process_responser;   c             K   s�   | j � }d }ytt|�}W n* tk
rD   t|jtjdj|��|�S X | j	| }y ||fd|j
dd�i|��}	W n: tk
r� }
 zt|jtjdjt|
���|�S d }
~
X nX | j|	|�S )NzInvalid method: {0}�verifyZverify_server_certFz(Error Connecting to server. Details: {0})r   �getattr�requests�AttributeErrorr   r   r   r   r,   r   r;   r1   r2   r<   )r   Zendpointr    �method�kwargsr   r4   Zrequest_funcZurlr3   r5   r   r   r   �_make_rest_call�   s(    
zJamfConnector._make_rest_callc             C   sd   | j tt|���}| jd� | jd|d d d�\}}tj|�rN| jd� |j� S | jd� |jtj	�S )Nz5Connecting to endpoint https://tryitout.jamfcloud.comz/JSSResource)�paramsr:   zTest Connectivity Failed.zTest Connectivity PassedzAction not yet implemented)�add_action_resultr   �dict�save_progressrC   r   �is_failZ
get_statusr   r   r   )r   �paramr    �ret_valr   r   r   r   �_handle_test_connectivity�   s    



z'JamfConnector._handle_test_connectivityc             C   s~   | j dj| j� �� | jtt|���}|d }|d }| jdj||�|d d d�\}}tj|�r^|j	|� |j
i �}|jtj�S )NzIn action handler for: {0}�id�usernamez'/computermanagement/id/{0}/username/{1})rD   r:   zAction not yet implemented)rG   r,   �get_action_identifierrE   r   rF   rC   r   rH   Zadd_dataZupdate_summaryr   r   r   )r   rI   r    rL   rM   rJ   r   Zsummaryr   r   r   �_handle_get_system_info�   s    

	

z%JamfConnector._handle_get_system_infoc             C   sH   t j}| j� }| jd| j� � |dkr2| j|�}n|dkrD| j|�}|S )N�	action_idZtest_connectivityZget_system_info)r   r   rN   Zdebug_printrK   rO   )r   rI   rJ   rP   r   r   r   �handle_action�   s    
zJamfConnector.handle_actionc             C   s"   | j � | _| j� }|d | _tjS )NZbase_url)Z
load_stater   r   r   r   r   )r   r   r   r   r   �
initialize  s    

zJamfConnector.initializec             C   s   | j | j� tjS )N)Z
save_stater   r   r   )r   r   r   r   �finalize!  s    zJamfConnector.finalize)r;   )r   r   r   r   r!   r/   r6   r<   rC   rK   rO   rQ   rR   rS   �__classcell__r   r   )r   r   r      s   
 
"8r   c              C   s�  dd l } dd l}| j�  |j� }|jddd� |jddddd	� |jd
dddd	� |j� }d }|j}|j}|d k	r�|d kr�dd l}|jd�}|o�|�r`y�t	j
� d }td� tj|dd�}	|	jd }
t� }||d< ||d< |
|d< t� }d|
 |d< ||d< td� tj|d||d�}|jd }W n< tk
�r^ } ztdt|� � td� W Y d d }~X nX t|j���}|j� }tj|�}ttj|dd�� t	� }d|_|d k	�r�||d< |j|
|d � |jtj|�d �}ttjtj|�dd�� W d Q R X td� d S )Nr   �input_test_jsonzInput Test JSON file)�helpz-uz
--usernamerM   F)rV   �requiredz-pz
--password�passwordz
Password: z/loginzAccessing the Login page)r=   �	csrftokenZcsrfmiddlewaretokenz
csrftoken=ZCookieZRefererz+Logging into Platform to get the session id)r=   �datar:   Z	sessionidz3Unable to get session id from the platform. Error: �   �   )�indentTZuser_session_token)�pudb�argparseZ	set_trace�ArgumentParser�add_argument�
parse_argsrM   rX   �getpassr   Z_get_phantom_base_url�printr?   r;   ZcookiesrF   Zpostr1   r2   �exit�openrU   �readr0   �loads�dumpsZprint_progress_messageZ_set_csrf_infoZ_handle_action)r^   r_   �	argparser�argsZ
session_idrM   rX   rc   Z	login_urlr3   rY   rZ   r:   Zr2r5   �fZin_jsonZ	connectorrJ   r   r   r   �main'  sZ    




"rm   �__main__)�
__future__r   r   Zphantom.appZappr   Zphantom.base_connectorr   Zphantom.action_resultr   r?   r0   Zbs4r   r   r   r   rm   r   r   r   r   r   �<module>   s   
  B                                                                                                                                                                                                                                                                                                                                                                                                                                                                           phjamf/__pycache__/jamf_consts.cpython-36.pyc                                                       000640  000765  000024  00000000143 13646101332 022117  0                                                                                                    ustar 00smasud                          staff                           000000  000000                                                                                                                                                                         3
}�^   �               @   s   d S )N� r   r   r   �./jamf_consts.py�<module>   s                                                                                                                                                                                                                                                                                                                                                                                                                                 phjamf/__pycache__/jamf_testme.cpython-36.pyc                                                       000644  000765  000024  00000000573 13646101332 022122  0                                                                                                    ustar 00smasud                          staff                           000000  000000                                                                                                                                                                         3
�g�^*  �               @   s>   d dl mZ e� Zddddd�e_ej�  de_eji � dS )�    )�JamfConnectorzhttps://tryitout.jamfcloud.com� F)Zbase_urlZusernameZpasswordZverify_server_certZtest_connectivityN)Zjamf_connectorr   Zjamf�configZ
initializeZaction_identifierZhandle_action� r   r   �./jamf_testme.py�<module>   s   
                                                                                                                                     phjamf/__pycache__/__init__.cpython-36.pyc                                                          000640  000765  000024  00000000140 13646101332 021345  0                                                                                                    ustar 00smasud                          staff                           000000  000000                                                                                                                                                                         3
}�^    �               @   s   d S )N� r   r   r   �./__init__.py�<module>   s                                                                                                                                                                                                                                                                                                                                                                                                                                    phjamf/debug_log.log                                                                                000644  000765  000024  00000052217 13647126434 015435  0                                                                                                    ustar 00smasud                          staff                           000000  000000                                                                                                                                                                         2020-04-16 12:21:50,709 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-16 12:21:50,709 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: Connecting to endpoint https://tryitout.jamfcloud.com; More: None
2020-04-16 12:21:50,905 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: False; Message: Status Code: 404. Data from server:
Status page
Not Found
The server has not found anything matching the request URI
You can get technical details here.
Please continue your visit at our home page.
; Exception: None
2020-04-16 12:21:50,905 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: Test Connectivity Failed.; More: None
2020-04-16 12:26:47,751 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-16 12:26:47,752 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: Connecting to endpoint https://tryitout.jamfcloud.com/JSSResource; More: None
2020-04-16 12:26:47,987 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: False; Message: Can't process response from server. Status Code: 200 Data from server: <?xml version="1.0" encoding="UTF-8"?><accounts><users><user><id>2</id><name>apigee</name></user><user><id>3</id><name>jnuc</name></user><user><id>1</id><name>jssadmin</name></user></users><groups/></accounts>; Exception: None
2020-04-16 12:26:47,987 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: Test Connectivity Failed.; More: None
2020-04-16 12:29:03,078 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-16 12:29:03,078 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: Connecting to endpoint https://tryitout.jamfcloud.com/JSSResource; More: None
2020-04-16 12:29:03,078 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: False; Message: Error Connecting to server. Details: get() got multiple values for keyword argument 'headers'; Exception: None
2020-04-16 12:29:03,078 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: Test Connectivity Failed.; More: None
2020-04-16 12:29:44,387 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-16 12:29:44,387 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: Connecting to endpoint https://tryitout.jamfcloud.com/JSSResource; More: None
2020-04-16 12:29:44,673 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: False; Message: Can't process response from server. Status Code: 200 Data from server: {{"accounts":{{"users":[{{"id":2,"name":"apigee"}},{{"id":3,"name":"jnuc"}},{{"id":1,"name":"jssadmin"}}],"groups":[]}}}}; Exception: None
2020-04-16 12:29:44,673 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: Test Connectivity Failed.; More: None
2020-04-16 12:32:44,321 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-16 12:32:44,322 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: Connecting to endpoint https://tryitout.jamfcloud.com/JSSResource; More: None
2020-04-16 12:32:44,627 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: False; Message: Can't process response from server. Status Code: 200 Data from server: {{"accounts":{{"users":[{{"id":2,"name":"apigee"}},{{"id":3,"name":"jnuc"}},{{"id":1,"name":"jssadmin"}}],"groups":[]}}}}; Exception: None
2020-04-16 12:32:44,628 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: Test Connectivity Failed.; More: None
2020-04-16 12:34:06,803 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-16 12:34:06,804 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: Connecting to endpoint https://tryitout.jamfcloud.com/JSSResource; More: None
2020-04-16 12:34:07,076 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: False; Message: Can't process response from server. Status Code: 200 Data from server: {{"accounts":{{"users":[{{"id":2,"name":"apigee"}},{{"id":3,"name":"jnuc"}},{{"id":1,"name":"jssadmin"}}],"groups":[]}}}}; Exception: None
2020-04-16 12:34:07,077 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: Test Connectivity Failed.; More: None
2020-04-16 12:35:03,031 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-16 12:35:03,031 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: Connecting to endpoint https://tryitout.jamfcloud.com/JSSResource; More: None
2020-04-16 12:35:03,372 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: Test Connectivity Passed; More: None
2020-04-16 12:35:03,373 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: True; Message: None; Exception: None
2020-04-19 11:00:16,373 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-19 11:00:16,373 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: Connecting to endpoint https://tryitout.jamfcloud.com/JSSResource; More: None
2020-04-19 11:00:16,621 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: Test Connectivity Passed; More: None
2020-04-19 11:00:16,622 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: True; Message: None; Exception: None
2020-04-19 11:10:45,414 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-19 11:10:45,414 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: In action handler for: get_system_info; More: None
2020-04-19 11:29:22,265 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-19 11:29:22,265 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: In action handler for: get_system_info; More: None
2020-04-19 11:50:13,563 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-19 11:50:13,564 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: In action handler for: get_system_info; More: None
2020-04-19 11:50:40,257 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-19 11:50:40,258 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: In action handler for: get_system_info; More: None
2020-04-19 11:50:40,258 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: False; Message: Error Connecting to server. Details: get() got multiple values for keyword argument 'headers'; Exception: None
2020-04-19 11:50:40,258 phantom.base_connector.BaseConnector INFO ActionResult.add_data() - Data (next line):
[None]
2020-04-19 11:50:40,258 phantom.base_connector.BaseConnector INFO ActionResult.update_summary() - Summary (next line):
{}
2020-04-19 11:50:40,258 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: True; Message: None; Exception: None
2020-04-19 11:54:06,084 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-19 11:54:06,084 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: In action handler for: get_system_info; More: None
2020-04-19 11:54:06,428 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: False; Message: Status Code: 404. Data from server:
Status page
Not Found
The server has not found anything matching the request URI
You can get technical details here.
Please continue your visit at our home page.
; Exception: None
2020-04-19 11:54:06,428 phantom.base_connector.BaseConnector INFO ActionResult.add_data() - Data (next line):
[None]
2020-04-19 11:54:06,428 phantom.base_connector.BaseConnector INFO ActionResult.update_summary() - Summary (next line):
{}
2020-04-19 11:54:06,428 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: True; Message: None; Exception: None
2020-04-19 15:11:00,441 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-19 15:11:00,441 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: In action handler for: get_system_info; More: None
2020-04-19 15:11:00,713 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: False; Message: Status Code: 404. Data from server:
Status page
Not Found
The server has not found anything matching the request URI
You can get technical details here.
Please continue your visit at our home page.
; Exception: None
2020-04-19 15:11:00,714 phantom.base_connector.BaseConnector INFO ActionResult.add_data() - Data (next line):
[None]
2020-04-19 15:11:00,714 phantom.base_connector.BaseConnector INFO ActionResult.update_summary() - Summary (next line):
{}
2020-04-19 15:11:00,715 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: True; Message: None; Exception: None
2020-04-19 15:14:50,524 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-19 15:14:50,524 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: In action handler for: get_system_info; More: None
2020-04-19 15:14:50,738 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: False; Message: Status Code: 404. Data from server:
Status page
Not Found
The server has not found anything matching the request URI
You can get technical details here.
Please continue your visit at our home page.
; Exception: None
2020-04-19 15:14:50,738 phantom.base_connector.BaseConnector INFO ActionResult.add_data() - Data (next line):
[None]
2020-04-19 15:14:50,739 phantom.base_connector.BaseConnector INFO ActionResult.update_summary() - Summary (next line):
{}
2020-04-19 15:14:50,739 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: True; Message: None; Exception: None
2020-04-19 15:15:43,488 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-19 15:15:43,488 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: In action handler for: get_system_info; More: None
2020-04-19 15:15:43,680 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: False; Message: Status Code: 404. Data from server:
Status page
Not Found
The server has not found anything matching the request URI
You can get technical details here.
Please continue your visit at our home page.
; Exception: None
2020-04-19 15:15:43,680 phantom.base_connector.BaseConnector INFO ActionResult.add_data() - Data (next line):
[None]
2020-04-19 15:15:43,681 phantom.base_connector.BaseConnector INFO ActionResult.update_summary() - Summary (next line):
{}
2020-04-19 15:15:43,681 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: True; Message: None; Exception: None
2020-04-19 15:16:51,635 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-19 15:16:51,635 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: In action handler for: get_system_info; More: None
2020-04-19 15:16:51,859 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: False; Message: Status Code: 404. Data from server:
Status page
Not Found
The server has not found anything matching the request URI
You can get technical details here.
Please continue your visit at our home page.
; Exception: None
2020-04-19 15:16:51,860 phantom.base_connector.BaseConnector INFO ActionResult.add_data() - Data (next line):
[None]
2020-04-19 15:16:51,860 phantom.base_connector.BaseConnector INFO ActionResult.update_summary() - Summary (next line):
{}
2020-04-19 15:16:51,861 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: True; Message: None; Exception: None
2020-04-19 15:20:56,091 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-19 15:20:56,091 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: In action handler for: get_system_info; More: None
2020-04-19 15:20:56,339 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: False; Message: Status Code: 404. Data from server:
Status page
Not Found
The server has not found anything matching the request URI
You can get technical details here.
Please continue your visit at our home page.
; Exception: None
2020-04-19 15:20:56,340 phantom.base_connector.BaseConnector INFO ActionResult.add_data() - Data (next line):
[None]
2020-04-19 15:20:56,340 phantom.base_connector.BaseConnector INFO ActionResult.update_summary() - Summary (next line):
{}
2020-04-19 15:20:56,340 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: True; Message: None; Exception: None
2020-04-19 15:24:33,190 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-19 15:24:33,191 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: In action handler for: get_system_info; More: None
2020-04-19 15:24:33,429 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: False; Message: Status Code: 404. Data from server:
Status page
Not Found
The server has not found anything matching the request URI
You can get technical details here.
Please continue your visit at our home page.
; Exception: None
2020-04-19 15:24:33,429 phantom.base_connector.BaseConnector INFO ActionResult.add_data() - Data (next line):
[None]
2020-04-19 15:24:33,430 phantom.base_connector.BaseConnector INFO ActionResult.update_summary() - Summary (next line):
{}
2020-04-19 15:24:33,430 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: True; Message: None; Exception: None
2020-04-19 15:28:08,200 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-19 15:28:08,201 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: In action handler for: get_system_info; More: None
2020-04-19 15:28:08,463 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: False; Message: Status Code: 404. Data from server:
Status page
Not Found
The server has not found anything matching the request URI
You can get technical details here.
Please continue your visit at our home page.
; Exception: None
2020-04-19 15:28:08,463 phantom.base_connector.BaseConnector INFO ActionResult.add_data() - Data (next line):
[None]
2020-04-19 15:28:08,464 phantom.base_connector.BaseConnector INFO ActionResult.update_summary() - Summary (next line):
{}
2020-04-19 15:28:08,464 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: True; Message: None; Exception: None
2020-04-19 15:34:40,412 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-19 15:34:40,412 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: In action handler for: get_system_info; More: None
2020-04-19 15:34:40,707 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: False; Message: Status Code: 404. Data from server:
Status page
Not Found
The server has not found anything matching the request URI
You can get technical details here.
Please continue your visit at our home page.
; Exception: None
2020-04-19 15:34:40,708 phantom.base_connector.BaseConnector INFO ActionResult.add_data() - Data (next line):
[None]
2020-04-19 15:34:40,708 phantom.base_connector.BaseConnector INFO ActionResult.update_summary() - Summary (next line):
{}
2020-04-19 15:34:40,709 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: True; Message: None; Exception: None
2020-04-19 15:35:01,039 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-19 15:35:01,040 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: In action handler for: get_system_info; More: None
2020-04-19 15:35:01,298 phantom.base_connector.BaseConnector INFO ActionResult.add_data() - Data (next line):
[   {   'computer_management': {   'ebooks': [],
                                   'general': {   'id': 40,
                                                  'mac_address': 'B8:E8:56:43:56:40',
                                                  'name': 'Computer 5',
                                                  'serial_number': 'CA40DBA260A3',
                                                  'udid': 'CA40DB98-60A3-11E4-90B8-12DF261F2C7E'},
                                   'mac_app_store_apps': [],
                                   'managed_preference_profiles': [],
                                   'os_x_configuration_profiles': [],
                                   'patch_reporting': {   'patch_policies': {},
                                                          'patch_reporting_software_titles': {   }},
                                   'policies': [],
                                   'restricted_software': [],
                                   'smart_groups': [],
                                   'static_groups': []}}]
2020-04-19 15:35:01,299 phantom.base_connector.BaseConnector INFO ActionResult.update_summary() - Summary (next line):
{}
2020-04-19 15:35:01,299 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: True; Message: None; Exception: None
2020-04-19 15:43:07,383 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-19 15:43:07,384 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: In action handler for: get_system_info; More: None
2020-04-19 15:43:07,623 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: False; Message: Status Code: 404. Data from server:
Status page
Not Found
The server has not found anything matching the request URI
You can get technical details here.
Please continue your visit at our home page.
; Exception: None
2020-04-19 15:43:07,623 phantom.base_connector.BaseConnector INFO ActionResult.add_data() - Data (next line):
[None]
2020-04-19 15:43:07,624 phantom.base_connector.BaseConnector INFO ActionResult.update_summary() - Summary (next line):
{}
2020-04-19 15:43:07,625 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: True; Message: None; Exception: None
2020-04-19 15:51:46,099 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-19 15:51:46,099 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: Connecting to endpoint https://tryitout.jamfcloud.com/JSSResource; More: None
2020-04-19 15:51:46,298 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: Test Connectivity Passed; More: None
2020-04-19 15:51:46,298 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: True; Message: None; Exception: None
2020-04-19 15:56:17,525 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-19 15:56:17,526 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: In action handler for: get_system_info; More: None
2020-04-19 15:56:17,771 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: False; Message: Status Code: 404. Data from server:
Status page
Not Found
The server has not found anything matching the request URI
You can get technical details here.
Please continue your visit at our home page.
; Exception: None
2020-04-19 15:56:17,772 phantom.base_connector.BaseConnector INFO ActionResult.add_data() - Data (next line):
[None]
2020-04-19 15:56:17,772 phantom.base_connector.BaseConnector INFO ActionResult.update_summary() - Summary (next line):
{}
2020-04-19 15:56:17,772 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: True; Message: None; Exception: None
2020-04-19 15:57:16,063 phantom.base_connector.BaseConnector INFO load_state() - State: {}
2020-04-19 15:57:16,064 phantom.base_connector.BaseConnector INFO BaseConnector.save_progress - Progress: In action handler for: get_system_info; More: None
2020-04-19 15:57:16,489 phantom.base_connector.BaseConnector INFO ActionResult.add_data() - Data (next line):
[   {   'computer_management': {   'ebooks': [],
                                   'general': {   'id': 40,
                                                  'mac_address': 'B8:E8:56:43:56:40',
                                                  'name': 'Computer 5',
                                                  'serial_number': 'CA40DBA260A3',
                                                  'udid': 'CA40DB98-60A3-11E4-90B8-12DF261F2C7E'},
                                   'mac_app_store_apps': [],
                                   'managed_preference_profiles': [],
                                   'os_x_configuration_profiles': [],
                                   'patch_reporting': {   'patch_policies': {},
                                                          'patch_reporting_software_titles': {   }},
                                   'policies': [],
                                   'restricted_software': [],
                                   'smart_groups': [],
                                   'static_groups': []}}]
2020-04-19 15:57:16,489 phantom.base_connector.BaseConnector INFO ActionResult.update_summary() - Summary (next line):
{}
2020-04-19 15:57:16,490 phantom.base_connector.BaseConnector INFO ActionResult.set_status() - Status: True; Message: None; Exception: None
                                                                                                                                                                                                                                                                                                                                                                                 phjamf/jamf.json                                                                                    000640  000765  000024  00000010402 13645671120 014570  0                                                                                                    ustar 00smasud                          staff                           000000  000000                                                                                                                                                                         {
    "appid": "f3c23540-5606-4e6e-86a0-717faf0aa403",
    "name": "JAMF",
    "description": "JAMF is a comprehensive enterprise management software for the Apple platform, simplifying IT management for Mac, iPad, iPhone and Apple TV.",
    "type": "endpoint",
    "product_vendor": "jamf",
    "logo": "jamf.png",
    "logo_dark": "jamf_dark.png",
    "product_name": "jamf",
    "python_version": "3",
    "product_version_regex": ".*",
    "publisher": "Splunk",
    "license": "Copyright (c) Splunk, 2020",
    "app_version": "1.0.0",
    "utctime_updated": "2020-04-14T18:31:25.089506Z",
    "package_name": "phantom_jamf",
    "main_module": "jamf_connector.py",
    "min_phantom_version": "4.8.23319",
    "app_wizard_version": "1.0.0",
    "configuration": {
        "base_url": {
            "description": "URL to connect to Jamf service",
            "data_type": "string",
            "required": true,
            "value_list": [],
            "default": "",
            "order": 0
        },
        "username": {
            "description": "Username, LDAP or local",
            "data_type": "string",
            "required": false,
            "value_list": [],
            "default": "",
            "order": 1
        },
        "password": {
            "description": "Password",
            "data_type": "password",
            "required": false,
            "order": 2
        }
    },
    "actions": [
        {
            "action": "test connectivity",
            "identifier": "test_connectivity",
            "description": "Validate the asset configuration for connectivity using supplied configuration",
            "verbose": "",
            "type": "test",
            "read_only": true,
            "parameters": {},
            "output": [],
            "versions": "EQ(*)"
        },
        {
            "action": "get system info",
            "identifier": "get_system_info",
            "description": "Get information about an endpoint",
            "verbose": "",
            "type": "investigate",
            "read_only": true,
            "parameters": {
                "id": {
                    "description": "Computer ID to filter by",
                    "data_type": "numeric",
                    "required": true,
                    "primary": true,
                    "contains": [
                        "host name",
                        "ip"
                    ],
                    "value_list": [],
                    "default": "",
                    "order": 0
                },
                "username": {
                    "description": "Username to filter by",
                    "data_type": "string",
                    "required": true,
                    "primary": false,
                    "contains": [],
                    "value_list": [],
                    "default": "",
                    "order": 1
                }
            },
            "output": [
                {
                    "data_path": "action_result.parameter.id",
                    "data_type": "numeric",
                    "contains": [
                        "host name",
                        "ip"
                    ],
                    "column_name": "id",
                    "column_order": 0
                },
                {
                    "data_path": "action_result.parameter.username",
                    "data_type": "string",
                    "contains": [],
                    "column_name": "username",
                    "column_order": 1
                },
                {
                    "data_path": "action_result.status",
                    "data_type": "string",
                    "column_name": "status",
                    "column_order": 2
                },
                {
                    "data_path": "action_result.message",
                    "data_type": "string"
                },
                {
                    "data_path": "summary.total_objects",
                    "data_type": "numeric"
                },
                {
                    "data_path": "summary.total_objects_successful",
                    "data_type": "numeric"
                }
            ],
            "render": {
                "type": "table"
            },
            "versions": "EQ(*)"
        }
    ]
}
                                                                                                                                                                                                                                                              phjamf/jamf.json.bak                                                                                000640  000765  000024  00000010401 13645630701 015323  0                                                                                                    ustar 00smasud                          staff                           000000  000000                                                                                                                                                                         {
    "appid": "f3c23540-5606-4e6e-86a0-717faf0aa403",
    "name": "JAMF",
    "description": "JAMF is a comprehensive enterprise management software for the Apple platform, simplifying IT management for Mac, iPad, iPhone and Apple TV.",
    "type": "endpoint",
    "product_vendor": "jamf",
    "logo": "jamf.png",
    "logo_dark": "jamf_dark.png",
    "product_name": "jamf",
    "python_version": "3",
    "product_version_regex": ".*",
    "publisher": "Splunk",
    "license": "Copyright (c) Splunk, 2020",
    "app_version": "1.0.0",
    "utctime_updated": "2020-04-14T18:31:25.089506Z",
    "package_name": "phantom_jamf",
    "main_module": "jamf_connector.py",
    "min_phantom_version": "4.8.23319",
    "app_wizard_version": "1.0.0",
    "configuration": {
        "Base URL": {
            "description": "URL to connect to Jamf service",
            "data_type": "string",
            "required": true,
            "value_list": [],
            "default": "",
            "order": 0
        },
        "Username": {
            "description": "Username, LDAP or local",
            "data_type": "string",
            "required": false,
            "value_list": [],
            "default": "",
            "order": 1
        },
        "Password": {
            "description": "Password",
            "data_type": "password",
            "required": false,
            "order": 2
        }
    },
    "actions": [
        {
            "action": "test connectivity",
            "identifier": "test_connectivity",
            "description": "Validate the asset configuration for connectivity using supplied configuration",
            "verbose": "",
            "type": "test",
            "read_only": true,
            "parameters": {},
            "output": [],
            "versions": "EQ(*)"
        },
        {
            "action": "get system info",
            "identifier": "get_system_info",
            "description": "Get information about an endpoint",
            "verbose": "",
            "type": "investigate",
            "read_only": true,
            "parameters": {
                "id": {
                    "description": "Computer ID to filter by",
                    "data_type": "numeric",
                    "required": true,
                    "primary": true,
                    "contains": [
                        "host name",
                        "ip"
                    ],
                    "value_list": [],
                    "default": "",
                    "order": 0
                },
                "username": {
                    "description": "Username to filter by",
                    "data_type": "string",
                    "required": true,
                    "primary": false,
                    "contains": [],
                    "value_list": [],
                    "default": "",
                    "order": 1
                }
            },
            "output": [
                {
                    "data_path": "action_result.parameter.id",
                    "data_type": "numeric",
                    "contains": [
                        "host name",
                        "ip"
                    ],
                    "column_name": "id",
                    "column_order": 0
                },
                {
                    "data_path": "action_result.parameter.username",
                    "data_type": "string",
                    "contains": [],
                    "column_name": "username",
                    "column_order": 1
                },
                {
                    "data_path": "action_result.status",
                    "data_type": "string",
                    "column_name": "status",
                    "column_order": 2
                },
                {
                    "data_path": "action_result.message",
                    "data_type": "string"
                },
                {
                    "data_path": "summary.total_objects",
                    "data_type": "numeric"
                },
                {
                    "data_path": "summary.total_objects_successful",
                    "data_type": "numeric"
                }
            ],
            "render": {
                "type": "table"
            },
            "versions": "EQ(*)"
        }
    ]
}                                                                                                                                                                                                                                                               phjamf/jamf.png                                                                                     000640  000765  000024  00000147464 13645400575 014432  0                                                                                                    ustar 00smasud                          staff                           000000  000000                                                                                                                                                                         �PNG

   IHDR    �   Jy�\  |iCCPICC Profile  (�c``*I,(�aa``��+)
rwR���R`������ �`� ��\\��À|����/��J��yӦ�|�6��rV%:���wJjq2#���R��d� �:�E%@� [��� �>d�d���!� v���V�dK �I���a[����)@��.�����E���Rב��I�9�0;@�œ�r�0x0�0(0�30X2�28��V��:�Te�g�(8C6U�9?���$�HG�3/YOG���� �g�?�Mg;��_��`����܃K����}��)���<~k�m�
��g��B�_�fla�810�������$���������������@ $wi��k  iTXtXML:com.adobe.xmp     <x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 5.4.0">
   <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about=""
            xmlns:exif="http://ns.adobe.com/exif/1.0/"
            xmlns:tiff="http://ns.adobe.com/tiff/1.0/">
         <exif:PixelYDimension>402</exif:PixelYDimension>
         <exif:PixelXDimension>782</exif:PixelXDimension>
         <tiff:Orientation>1</tiff:Orientation>
      </rdf:Description>
   </rdf:RDF>
</x:xmpmeta>
ޤ�  @ IDATx���Wy.���V�-jV�,K2.����Ʊ)�C��_ ���.	-� !HH��\������J���bl\p/�\d˖���v�u��<����7��;�E[����w���s������y��`RB@! ��B@�QȎb'+! ��B@! ��# �AA! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@���q�	�! ��B@! �Au@! ��B@��4�t!�(D~�`���*���	F��S��V�� 8��1��1��-��B@!0��qk	2VȐq.�R!P_������*��N�i��N�+�*�Gs;��d�SO1�� �+�P�����fʡ�B@! ��ӈ�����6c)_iƁ�?Y	R��!1\F'�&~�M9�Hv�<�	'>�1މ��
�e:�����7?��4|��~��B@! �1�(����KvB��LF�Lf!�5����M��H�*�V���-���������H�$)Hg�����~G7 2bM�B@! ���~�8��r�U1{n$��F���JK��FtE�;:�7�HB�K������֏�n,n��d!�2i���= 2f�48i�! ��B@Lb�
;��dC�ӹ�.O"��ql 	_�g�d2󐎪�.�L��#W�����{�oZ?���-���@d�C�r,Ӑ)+2\��ґ�B@! ��t# �a�%��0f˱Ħ�σ���mr�Ì��!�Y�gI��(���7W�;S��p@	�-�8��"?ܲ0w�\ɷ�!��B@�9���1$g�6�!�k�<↦k�XnM����	�0�2d�����c �!�@\�A;�sȺ�XOO�e�C�	he����1Q� %��B@!0S�0� �ⶡ��A�[�s��68��,�m�s~�r��h�9�9��P���:3�Q�~ۻ�Y{l�68�m�����&0seH! ���1c,>2yk�օ�v¦mq�2�j s@Ҹ���@�t)��7�{�Q�)�����dp��+c�������m�m׎mX��&(�ٚS��! ���1c-�|#��Uv��/���V�:be�-�8���\pz�	H ��;���$�R�<�p`Y0Z0\Y[w�I֘m�g�~��2H&���B@! fb�E\u����fgnⅤ���b�l:L����xC#�'qC/�)�,�{¾h8�^ ���	��L)���t���!,׸�V��d]ݽ�oד.���b�B@! ����q@!�D?�N%{���nƣBA�r=~' aF|՚M�����A�6`4��~"PR��<U?���/*π	���%�P����������f��8�MD�]�G! ��B`���5��wI��,6������D���l{�X�N�"{�e^�.j�Υ��.m�B@! ���~�8�|y߉>|Sb��F	�M����]I��rl�o.�"_PpLQ���a�ѱ��cO�܇!%��B@!0��"K���C�8�Gah��n4��ҺT,o7�3�/-i�_\���C�4a�C6��ҍ�7�eM`"$p3�� ��B@�#���`%#���8��߀3��T��7JKM �;�`��c0YHu����5��%z�z8˫B@! &1����h`�q� ���fO��̥�� ��{`�L[����i"%��B@!0]�qH����H�F"5�a�6m�8�k\��C�'Y%�,Q ��1n��
e@CJ! ��B`������`�<l��oxH����d:�+�u�%���B0~υ3e������>0�q��AL��!WB@! ���(��!���)ƀD,�q�t������lui�Ħ�8ܗ���I�@5�z�`W�,`6I�$u(�'�B@! �Q�	��4��f��Q���%�R@   Q����L�K�x�6ot�:x�-��8��q�0��U! ������a �R-�J�6��H���d�y׀Q����C��w�����]H�0p+! ����8mY;�:�et��T	���Ҧ��ƚn�������|�ݔ:�1!�I�dȀ�!�<ꖌ�m�Y˕v�u�e����iw� �Ԅ�K�R��jJEM�u���K�H'������*�Z���d���}�y<������҆
C����G���&�ʃ6	s�������9�q�j����+EbX��J3?+KU8&h�G�a�7I7�w��	�(�B�:����J�d@�u��V�Y�@B@!0C(Me@����,'�I�aR2N��7�i�������4"�lwKes��6�3${Ә1��|���4� ��/���2;�o/`as6���T�?^�X�<-f���#;! ���"PEZ<����8YArC�;��J��\2�0*r�%�qo����?1�%Zb����%�?U	�I����<��zERD����dXG{���B@�Y�@˲[�s���9,O¾�<��	L�tJcp`�%̞��,�C9��b\L�V̆�}���HH�I	�#�@ل?X�\�@����ߑ^�
! &	�t?^��ΐ���E��l�Q+mig�uvt��e���immKl���Ӑ����l�n�Dz)�J�q�T��
��G���'��{���
@��T%K��iXϼ��b�:W|S��q@�4>�q�}7X�K1����556���9��2'����� ��K���#;t��ؓ@��R���,芥K����kg�u��?f�5��Xks�577[�Ɂ1 �={��G�G
�.�YN���F�Ü/♓�p�Ryc�	b-�=��=��%g�t�dC)�p ᠂A$�Mo�mjh 3 &��:F��׮Ҟc���"w\�ʺI�\�7&��%%��ӌ@2��C�L!�a���a����.����SN>�^|��v�	σ�F�2����`Ov�tH�(Ҋ�ʒ�P������]b�7E{%�iƺ��Ѣy������ρ!�@�~�8A�LB��#�)�bV�A<�`�D��97��8`���|p�
�Υ��B`�e�~Ҡ��ȕ
��.Z`�y�k ]x�}��ֶx1$d����F�AЕ;)�Gė2BZ$�
%3�"�RkYT����%�an���Uu��g~٘!u����Y]�h�vRB`�`d�1z�<Zo �)o���XӺ�6��.x��i�F[�j5�����Z��Om�[n����.۹s��@2f����<a�p���%�B@!0@�l��~H�)Q.�������^l�z�;�c�B�3N��Πy�cENc3�R)J��V�\�~d�ThsR+�aN�l�7C����Zo_�x"�fS��̴r�B#?�L��Uk썗]f�}��¦�FH���:V:kV/��x�<�v�P��}����o}�z�a��'�UIM�B@��G �>�{^��_�׾��v�ZH�AA@�L�_����o�q�b�������cW�t�E#j�/0b��qY	bt�8}_iC�7�a�>\[m�)���j����)j�b��.��'#�6�(�f�`���:R�#�W�+"��Z�	z�x.h�,T���8=��N8�x��O|�:���V��9'a&
u�"l/J`�x�;Ｓ��/>Ӿ���iW\���k��B@L3a	j�֭]c��`/8�$�b0NV��c�fg^.
c�;���ѿ;�@&�B#��Ӝ���W$s5A	ѕ��'v��M-����L66����WeHR��	���kd'Գ#��"�q���!�W���E)dF�ኳ܀����(��d�����$a���*�DL?�B� ���~0Z�,ҙ�FP�����@1��N��I���}j8�H\x�'��ܐpB]�O�x�%����^ko��yNpA��z�4̂��p־��;�n�V�����m����-7Ms?*J.���~��B`<����1��>���e���_k�MЯ���;��6[�lY��!v��#<�@���!�GK_���`|���k������vb�B)΂<�	�	�Ь�յ�O�!uG�o,��Q(za�CB�ᄓ����S>�>���0Ϣ	0�n��u���wآ�6l����w2`r`��ȓ�["�ʎ�,
'FQ?�l���9t�$L�b�x�Dׁ������<������4ao ~kuh��i`�j��D�1���H�eL)�޴i����G�&J�/z�x3�,�54�h�|��`�z�_����
�oR�[�>��B`d*�/���}� k���[��q��>��vɯ���a��lKTKw.0����1�!����G��ܶ�0��w�.��R�����p���m����>�6*��(U�U�\��l
g�q?燳`��ڢE�x:l��6��Z��D�cy�gJ2�����d-t �-��V�ӥ��Y2%ܪ]��;� ��:����a�lܶo{�p�e8)��A�b.��48��ߙ;<%PǬ[k��̧����|.��Y�A�z4�BŬVc�y�^��K���>���?�!�Of2ύ�P��a�W! Ƈ@�K�)�mjn�ťK;���{��_;���8�F�>QX�*�B@��V��#����
&%�$�n�> �|З��8���zy(տ(-��3�����Luˢp2?�f���V,_e������$��ʹp���p�:$�`>|I�	���H�&���v�0ZN�� }��x��H+-�j�UGo�fHI�>� D������8��H.[�ҭ_��13�"�w5��B�r��4$�Y�!��mmm����=v�/�C=��O��q��B@L�8��P�Z������>�񿰓O>�O����=qn-����  ����Pk �!��q��~a\���{t�$B��u�X�=	��^0!#�X�,\�nK:V��U�7FfA�!�<�)}��q B�#Q��s0�4/���\$f ��}L/«��B
'��A��l<O$��X29���X�����\g]]�l��[�,�9��=n����4B��r�w'n���.¾����a���Z����L�%�8�Z��^������x��i`�q���(�fz! �����]b�18�yh�~�����S�4p*������I��Sjj�058+�"i��֨��L ��@���ҀB��2~��}.3ʀY�Z�[}����})f��0+��z��$2ct;��>P� ����$�g@�;4&�ˆ�,�0Qz<����wZO��wZ_i�8"aL����Ͻ����r�&[�z��۹��8��{U�~�{٢��f�&l���y$&;��A���(��Jcad&�_.�6X��.�iK�^}����ƒ������ݹ~��B`�}ka"��e����w��.	�A |d�'l��������r>>�sk謑�ѭ���]�VL:$�1��ʽ}����l�ck�$���1����dZ-�jG��h�?��<j�5�iĒ$��DF��?�x������w��c�H��S4c�f�@b��ӏŎW�� (�U��#?p�FpL�������l6�z� ~� {��_Uč��cX�5z�Kn�n9�k֬vo�Q|�W����B@�@�c8��t��b\��/����7�.ƽ"A�
+2)�	j1	�q%I���r8%q(�C_G4x�{R`E�����ޞ�0�:q4Tvt��q=i=�0y�*���K�eG�?�,Y��X��	w�uf���c�<F5*L��Q%d��ۉ��vA1�,�ID�I|3}d�*���D����5b��r;��9�恧JKӄt�*O?b�|7�v�O<� Ǟo��>��xᠿ6���޾:J�P�P(a����N! ƀ�K���z��7NԼ鍗� �n� ����>�l�n���4.9����s< KU��硱�yX�ӑ�@x��Lr�'*��r�]>�#V�8s���jmKW�	�!��:H\�I򛛝��"P���$2�?I��;����
�F�Ws13��K���rL���DOY�-Z��SM�|'�g�"'�S�<����̉I�r,����}�k�X�i9tn\aT�(_M`LZpS��G��lF�.+! ��b��c��gٯ��U���p�gd8��d��d�8��N ���B�0p�j+�ُwԘ��Μp�8̜���)9��7 �IB� �}G݊�\FԄSo��p��\�����X���M����t�~]%�,�^��ˠg<��!�P��?�
�AT�I@8~�q�:l�t�I�3�w�t��7��`ق���	�cH�����˄Z[��k4�Q�:+H�d/����9�97��x}��ػ��N�ؽr,�} �)y��(#��\2x�v�7��{�RD@�����"����S�е/&�y�I_Ξc���,�dE�@i�I���E<`��m�I/�%�˱�U�Ǖ"v���q��?cgO;����C���ֈ�=���x�흏@g�wID/�0ovX�=Q��gf������'��C|�RY���;�>�^^�L�h�>$݇��ڧ0�����b͡�nԭ�`���QJN͘�@! �#�I���~k��7�K�p�9�g�МT� ,W�j��)�B5�5�]��C]�(P�Ѝ#����!|@�q�I�O,ֹ�[���(Ǚ�P�. QO� C�ϡ�}s3i]."���L�xRRؔ�.�/�a;&�̽<j�����w�-Y�*���ڏg�$�J82 ��z��+)�J�{
�AKZ��_��o�9;�I␎���V!�ŵ���zz�m�"�C*ɒy:���Z�J��n�D�Tκv�&m\��z@�U�O����*k���Q�o�F�)J4�s/n0�ŀ2�cX�`Z:g��IA�U���B@������Dģ�Yk���cCߊ_r�yR��8W�J)��>��)�4�	�����G6o���y���.{��m600�L�� /�<GV-ȵ@�&���Au`
�vC�e����hn>���Hm��L�-[n��=��d���9�co���{>���p^?À�����g�?i�Lπ�G�h�韒�	)�O�1���Q>H ;�7��� p��؋�<ե$ꉆK_��~y������Qr�&~�P��8`;w����d��3^���R?B@!0�_��|�uv��~}���w����Iϱ��/�|���K_��=�̳�*%���}O>4�����yh.��<,���29}o�$�\����|�~��Cc%!L9[L���h�8!��OIjhY`6����VZ?�����SH�Ù��*�)E�=ʛ֞�����=�Ip	6�&��%�]���8���AHxZ�r�g�v�x�v>�A���%.���B`p~�K�^�W�:��uգt�>������^���{��_��?��k��%�~O*�1(�qn�d>��t�]`�f��N.����M�g4s�ϡ���g���qf��&�'�1��4���\C�-]�7&cX���M�� f!@4�~�`����ؐ�|��=��CCC���@-��T|�v��o�K)
.X����F��y[4�1�� ��B@��A��c�����d��Nv҉b_���Ѩ��xg8.`�����o?o�\{���/.�a")�W?prH�6bjc$���SZl�d �~G��>�L	Wl�  �Ɓ{����k�	J�l���������(i�zt�R�q/7�]�����#A���B���An~�������o��3�Qe=�s��e.��� P�(��/�s��C�<�	A�!��}t_��}��_��t�������Ɋ.A���;���$P���I�|v#�a>��杄	zv8��X�Z?�p �����P�D�+6`g*H�a� TZs+NP:�d������D02;~B��[jn#��
MV��ܩ��7��?�,|�օ�A��a.oK0r��'���w!0���������fC��?��_RB@!0Q�p�۩���G��2X?x"���î��r`�ϓ�����ﲛo�	z��8�������%���zb R5�P"9�4p|)�4�<���ԁaG�t.ip"��1�|�<�M�l�Ѷ�c��sp���$R
5�I+��Pqƈ�#)Jv��c���Ν���R7ǣ�X�8��c�x��3F�K|�i��|�[W���ދ�K�������)����p����ݖ/��t�����i>���_�u݇��>�y���]*x��ј�Hq��R�"PQGu&K!0Q�ĚwX~ԋ�xct� 1�j��<�e���"����Ŗ�q�i��)V��=U�D&�b����.eq�����|ζmƏ�eU�&{a\���Xw�Z��'.y�^{>�U]��k���v���F�ǯ���P�Sn�/! ������:�(\���z\�\���fw�K:v�7�i��b∄E��-഻�"����8��b��L�A��3��D���J������cu0\��{��%oM��}_C�n�*p����D�w,�y��_������}���kg��`�d]s)5 G�H�&�s��{��7���!�Ṫ��q�P����! �@U��w��ҷf��݆	���e���p�`r���������8I���w��u�g�ا���6ב ���0���g��>d�c�M0Li�R�`௭s�-j��!�;ϒ��Ăg>�\K'�#���~A��������0��{�����i�k[�00�hd������ܾ���.���|�t¾�\g08�y�%%���� ����v\މ#���Xs�p�z��G��s;vZ��&h�=b �#�}�q/r�7f|Y��ټ�tL$U1��I��I���>.?�h�4�Y� ���P}cN�<�q8
��p�jO/�����G?���X�Ԏ?�yv,�eK�YsK��޵�=��\�������!���=� �Ǎ�|0(\��&�z	! ������t	0��8YS$��Og��?�#�1����=n��z}�B�}w����堍�K���1��� �����kĄm��=���\QlXܸ���8E�8m	���F,Oj���Uh�aOeTXM"����O%�[a���~���=�x��}�)����U}��$�4�A�*�� 
K�%˗�/���B`|�-Y�R����Hz���臝i`�o��C�iz4$#Q�J�]֧W�Qfi�8�ѐ��!���MKl����7���%{T4�,1�`Sk�֬Zg��<~��2�c��w�S�)�P������k�.j~k��	�! ƃ@sS�����7�s�g��-N?d�g-��7����HTa�Fr*s!0~�d}}x�쏌����xQ�hhnj�U��$��_>��B@���@NT�=:�V􊙡=\� iEޏߞ@x�N���(�an���v8`��`֎�"]�q�˚�4p�ȲGAR��R�t̠�()B@! ���!%	��`7h����\��Gjr�0�x*� �υG�=ݾ�!,S���9��56[��h����I��f4�04�! �����#�1�8�Ϟ=X��=��!|���$f1LӞt1�^�#�(�΅��+`�t���PT�kh�}M͸&ǻ������!�I+��B@�"��cN0���~�
�IJ<�]jr(��&7l�&��W����s ���H#�g,K*䳶hq�5�� i�q1
i��B@�Y���tA�y⾆�:�Z�W9�1u%gD �?/kۿw/吾qiĵ�d��i����P�@#<�&�oj�9�w! ��B@�k�8��⟺��޾�^;����@��J�R@����%�`�2���s��_fB@! ��������T!VA��M
��xƯ�/�D%�����0�,,[���yi��@h�RXe$��B@�)C@�ÔA=�#�g�~��# <Bػ@f�3�9����G���D�Ո˚�V?B@! ��|G N1�y����Lf�us�d�9��J��k6V߉��@��fl��ؘpp�.��{�p�9Ě��$��pQ�5� �h���6�4/�|�ٙ�p*�RB�NF��zUp����uu�J�<)�0g3ݠ,k�j��4.��m�8U�j��T|՝T�IuWsϔ�.彔�ߚ�%>�*�H}%&aF	��4Ki�K)�.E�I8U���L;-K��&��y�m*�	k�����r��"&&e4�v�W�x�#=S-�O�<�}St�N���p��T�@���e�
��lO�O��̜6�0����f����F��O^��~>?h9dC`��c��^�=:d��x�;�#W��Drk]�Ě[��~�#��ޙ�#�'�>G(���Ɛ�$3Z�r��}y���5)�$�'�wl���rDB�s�X*��x�F����F����2<�̧"좛�A�׈�����x��GE:���:MEt�����#d�����=ڲ�*~ �Ջ~X�*��`��H>a�ʵu���H��1��� [�9���O�C��`�{�s`r��3�@����g`C�p::�9���IL�=:2� ���d P9:��[=���XF��M�i$L��x�ȣ�*V#��J�G~^��* ���0'1�*�T7�'�z�T�H���6�d��#l��Զ��[3^�#S��(V1󢘏L&)�e��c�*D� ��>`��Yc�m{l���H�\��%I��Y�LdhD�	�5Z{�Rt5�J��^҆#Szs=�4�?<�qi�m�6�&WS1��X�>"���<pc�cR���<V��_bV��n"��UM��T\�Xf9�?�p�/e@�O��Qn���G����NǸCY�p))\NZN��TLC(�RX�;��9��q�����p�d�p���)d�p�cDO!��2�h>���_E����H歄x��2Y��1�^YX�"�cn.9�0�JsZ����P)p�0��B����e�<�(��!�w �}I�J���C�.�X Ჴs�5�,�[2 p�,!��aZ
w�FJ�|c����h�$VzX	CO�/��w��Q������<�G�}�ӑ3=<���V�Dƭ�x^}�b=+j�!����B�M��)U6)�0���
�j|�(�;�%_AW��J�#�=<���!�%��w9���'.}��Z��d��aJ�R-i�Y��M8���B[p}��c��	��Te�(��W���%?�Fg���-�Ra�W�C~�מ}�	��^��A\v��}ӳ��,�1aI�����#��i�{"ARB�.b�����otV&ɸ�_�{�.s4;>J�#���1�' d�H
.J9�9�d�`�CJܗB���we8���qH�fi"j^�� �r�^�{J;,�P����O��P&A��$��I})����ʥ��N$oD��PRn�9�&%��*yH�3�I�1�we2"�S���,1���KxW�71lwL��E���N��O@""R��޺�3x�xY���M
���C�Y��Y������+G�8̫��̢U�b7nj�� /���i��ރ�g�|ǁ��B>���	f�7�gpSS�[��� �9U$fu��9���"��rI�N c$�|�Y]�pP��*�}�!!���-���9�$l/l+�7r���&!�p��x0�+�1Ȁ��d��-�B�#�<��᰽3P���a�p���0~��n�7��O�Ya�Lc�CBX�:I;�ť�Ts��b���C�y=���x��9Ą�� �yKB�`︢,Bɲ<�/�7`?�c�r�	�n�(	�'���^xO0f�鞉��K����a3NJ�yf�d=�W��W�Ӂ)+�{�1��A���Р�A��b�2�̫���b��	���_~;���~b>Y����EM7L1oH�z�x�f���28���Ԅ:����Ў(��W�f��ۤ��rJl+^1�`�_�a��,�:̣���I�3ݦ��i>�C]pX��CyzP&L�T@@��j¸�6�YH47' аHBpY���������F�	ǥf��$�� �q[��pc4\�l�cG ��4����u����^�9@��:|�j#k(wj+|�#��l`��5#Uy%���!�@�@��i�pP�6?��|��M� 4,Zd-�M֌6��܂�F�ցg���p�kko���6[غ�r��N  Q'����l ��@��u<`{��}��۾���}П������o���݇~�,�ʆ�4��@�!��O����.�$�����A���buW3�ΰ�(���� ����aSr�p��	�H�������'q� N�����ɖ,Y`�X>�`A+��Yi���z�i�N�~�����b�����ý�{�.{j�vH�w��ف�.���vdfXOB;u�����䰌��N҇�b�xxP��+��8�������l����wK��K�غc�Ygg����c9m�-Z�nyx�Q�����n<=���O�n��={����Cv��!�y_?r��t ��>�2��� C��m�,؍(��!��C�*��0��\�2��M,p
���拓9�Ә�ll��"�U�#�%X���6lM�Qb�9�!��� ��� �F?O�D��
�qPM7��
�	�0(g(9;�kO=��܍������!5)��;�Y���A[Ҷ�$m�p��"����ϖ�(^�d��X��	*,28��Ё��������	����%Gn������Ւ�GI�1�>�	�9�l�ls� ��oz�mܸ��]��Z�D�ǫ�����ֈC*���<\G��$<��N��i��qk��$��o�u����l�ν�u�۲�Q{�'�'g�}�Gd$<?�������xP�y�L������0�_t��>4	�C8,S�9�d'Ҡ's P=<�x���xs �"֡5pi)g�s ��v��'�i��j���g�-_����� ��	a�L3���� �"q;�Ў���^۵k�����=��v���{��{����.��Or�N'2�
4�e�m��u�	u����.�y[��j6n��O{�mڴ���Xf	���܌��K&��Kx4rr���`��qzn�N�&�����]���|�����r�����9O+���{��s(�|�]�����7[낖�I�O=�`n�����:IIg]} G=Y�j�}�	��څ[�L]�~\u�uv����� �����;!�b�G9�\&� 2M�γ6`��<k;��
�^rM�I�S)�t�9g8ö��Ӈ����(J�I'��l鰗��<��?z��#X�8�KU�§�=j�p �ß������?`[�>f����I�m��	�"�}Kk#fAu�_x��{����S�o��.��p`FV��p��\�6�#׻�HB�C\���0MMkh[hK0;K�-*�S���-��f7�p���֋�>J&�|f	+zn<��^Ȼg��0?`_t1�Iypv<�[�@���*���"�d�͏ږ͛;��T�� �=�gt���t�D�^ho{�ۭm1?&�qI��	�n�:����Yr�d|� (�����_kǮ_kg�q���ͯ�C��v���mW]y��X�!�!Lk�R\��v�}��F(�Y���֬Ym�^z�]p������;9E����O����	�wȷ�Q�I���b0�U���6Hh�����oz��>l��v�}��ߵ��b=��\Z�F��3�Χ2�g��3�v��gB*ي�2�$�*����b�^�X>�`-�����ڂ>��
�B,I݊���~~+�c�\#L��m��P�C1��L:+��EC�$ä��Y�eM��*������u$��H����:����f�z��.�h��G�Ґ��V�»Z���:0#�g��f��� ���Iĸ���za23=~���b��6DLm��͘�Gb��<�-�R�r�5��6m��O:�6nXo�m�h�sL 0q`���8P��g{.�|'�
��5?��^�����$$����nr�1����`/��� $>���V���_�C�/�Z|�!1 O 5�P1H?���w�� Z1���~�]v̺5N�������o\&w3��^pF;�Q�e�s��[!U:��/9�N{�iX����&�Lf$�����iMjI� ������3��+#��X��u�/l����M��W��~q�/�{�����.C�<�I����'��|�9±�����ε�N��x��X����ե.~�H*�;)$��;��CI1�t�����m��&����X����_�:�m}|���;��?�����/[�8�lQ��3qu"���� 5~��/���*9Ρ�!M!���e���6#�x԰v�N�x]ys��hGf�ۈq(1B���ˢ���@l��|��`����
*b�j�F]��"�K��8:�ZM1M�Ǝ1m:��Y��+��6f��U��a�V���;l�������a�w6�!�	Ot�!H�*�Ӟ��V��l��5>�B�Dz��  @ IDAT��b��"�X@��Ph�	+"꣏��pCem�����:
�6D0�ދގ��Ľ����l)fNc;��-ɇo`Eʗ-���x��ꕯ�E�M��~�y��PXR(����dQr]��M��r�2�e�7!��c�{��s��v��ڻ��z{��_�w�馛��I:(�0��?F_�>	���o�s(�w,C*\�#M�o@)I��l�t�&�2���C
�! [�- �p
�pCr6�@��㎳?��?�u�V�'v�I�x�D�=�t��&)��!�T:�w�,�y��en�KZ��_d�\���M?�/~�+�@t���l#	�@nB�!q���z�8R�Z�Oo�r<�0�(�{yF;�[��ﱗ��bkN���i���J%>1,�C�vU��<Dm"�pgM\��X,	[Iĥv�]�����]���Ş�$P�@4�
�r�Z3�!�)8���*ƙD��/������0�!M�� bD?u3أH�.�.ƚ�V���k\A��M�Ed����3�Ej<���8x��+C�t�f:�v���`kC��X��e���鴼c�F�<��tnJ��L	�БS91�Y���\.�q]���{ i�vhn�(C��u�Es����f����V�)��t��S�
�1 ��;T*�����10y]�V��q0t�z
��ͦ�Dτg�����<�����M <N>�;��3��y� %	�Ut3�74���~v����?�c{�;�f7��C,!���	�E�����#bs���>dܩ8�9�0�|�L�y���W�蠎7+�S2��Kq��g �ऩ�Ɏ9z���/��^�k�Ғ�U*EuD8q'���$.#ʂH����Hƾqŷ즟�k�r�X�CQ��ϙ`T*���ȣ���a�X����?�|���C���.L�1GN�z�ű�簬��3O��|�KX��<?�'�=�,2��n"/���+�K.�J�����!0UI��x�}�a�w�c���q�2b�K�@�P�b��3|�PV��ww)�p�|QL<3���|W4�����eN��a`�@I�9.E����85�{~���l�#���z�t���ց�;b�i��	k��	@n�@m�"C-����E��>�Ti9�N5��~�b9ߜ����W��5x~R�vkƚ��$�EF��~*�:Yq0����͍kW��w��v�^�%Lw�W�z9_�F��
��!�K� ��\�l��������d���i5d$O8a�}�����;B���AF�:��	����?P,7�ȶa�1��;����_��%���dH0'�:�q�cxQ���|�t���"��������Z(�F�(�a��	*�1��!�X������7����.����?�ʑ�d�xS��T*!�N�΄�(�1^�l���X*��9;�����p��e��4.�S����W4��w��'��NO��إ枰�3��h;(t��F&�s�/�
��н�m�� H�D4P�3�1�C�V����^���;���t��E�!�y�w�f%��R�0̮_<���ԟ�ͥ/9���k�o��K�b���}��Xm�6�o�����W��K�&��36�d�_{���������?�[n�����(�x���e���1���O(���˂@Kb��/7�^�%l�����5�{KⲜU�_����p��0��?\�zM�e�Z@ _��W��U��_��=�c���ADY��:�9�,g��k`���Mo������"�8|�>�D��O��x
����H֧���<蓟��]{���+�����@�	g/���4"���c����a��eOC^���}�gm��L����0x�a%b��)�`��, �$+x#���y�n�����$���U���<��Npt.;������cږ��,S�a?Hg��<�c�q:2L�*t���8���ጀ�S��Y��$V&���J\|
�C����>����n�K|i_����m1�3� �8RܬJ�	��I���[b�����}�>a���(������i��))��J�sT�t��	$;@�r��{�=�[��P�r����b��	m)ƍ��:K&��������������?�!���/��M�m����ʙ�p���>�a��w��zq�O�"?�Sᴪ��T�y�x���ǰ�z9��P�����O}��ƣN�e�K:�0n��x,������aH&-�a�E��<d�=�0��6U*o����j�<��+��>�:2!��;�n�������Cք��9\�ֵ�i�|�����,�ۃa
:�]��3�Q]�tD���d�������q��1#`�	�{V#���R�G^���8����2�ª��G�6�d ��6Ai���}Sb�xf�l�س�Ph<��R�if^ч!�@p��I'o�����[���a�T+�jfcO�L�sǺR���X����ox.3C�0�	��W�Ta�s��0>J<�z����wIP:���P�ǟp���V�X���z���5aT[�{[>����iQg�b,� �M?�8A��EB��p��L����sR�|J"����ן���腧y"Ki/��S1)7՗��&4A��0RP�S���;1HSq��;�mOm{�2�p�O��:gt`��=2~���3=p��ǿB��������������n���0�̣l��0²���Ƕ��޷�r8w<���K�:�:|Wd�<l`�YJ=:�e���03�ǀ2ճ_�S*�َ k07���ǟWT��U�9��~�=�����~��h�y[a;�$�8�J�t�7��	i��?��\憎�*,��iJ���w��>�1,�X��Z�#�����O
�M���R�&^|���/���x���e��L�4*�*ZD�)z�1�by��_,�P�܇��e����߅��d2\��,/wd�/\蒨SN9	��Sw0��d�>���4��T�X]�D�%dtä2�|�ąt��څ8µ���_�BŠ[��`����"��>&5�YX��Ƶ�TN��S�`�����{���-8"Q��Ć�@���[��|N=LGT�3�+ߑ����E�'��dI�cÂ�d8k��f9�e�,�cY�!{�;��;���v`?C7̱I�y��'��Ց��?1]��i �Nr�ʵ�@�;H3y��a:,���"0]u�7���
��h/Ooʾ���r=����jmqz����C����F9��Ҍ�^|�}�ӟ��׮����������|U�O�Pf�>^lF����p/ޱ�cx���p\�E�`����T���:ㅧ /���<5�R'�}��C}8al�}�3e�u�3!�!�e�{��3�`�ħFzV��}���s�B8i|��@[���
���tB`�T��	�6��{Ϛ� t6ܰ����˅�����~�9Ú�|?���}���;��=���T�P}I���0:[LV���ָݙLB:�L�ײ`���z�ﰝOm����������]O�o�4�#��?f��~	��,%Oe/;0⒌`���Ӕ:q��B`EO��N���D`�I��M�חt�-s�4����^k۶m���"����kؖ�l{b^�C)&��'��l��U�P�1;����x;�9iA���#�B}��-��:;�O?�Ǩ;D���?ps.b�V�R��2�d#�^p�,��u�p2�K֒������f;�y���9�ɼp����d�����Ѵ�t�����$\\G��Җ�(�w���ɓR:��0��ء�N�3TaM-�=�\h�Yг���;��;�|�����,�nBqj�s���ñ����KБ�����dzܷЈ���	I�ﴭ�e��s{�W��m[�éI;�`F��,	����@��(�z�J}y�ÌOj���e�WSn�$�L�Ð@CJL��7��XNB����o$z9{�t���eW]}m �9���&+��&lZݕ��>�b���%7��?���|�ɐ�BR7q���&�FNRzp��p*N:眳q[���� M��ף!r��R}qb23^Li�ñ,������ŝ%�O�6�p����:������a��0�#�xOD<�lf�ob��\���>�i�hks���1n#!0Q��J�� 	YnފK�fҗ��Y�������a�Χ�L@�ݍF�M�v��d��%A��Ǘ��v�o'�)!��6�U�-��cQy1[���{��^,7���C�}`���d��g�٧�-�kw�y��y����ݷ۞OZ�<�!B�����1ݼ���CSV<�5lX�7:���Kv�|�!���Y���h��6�y+&�a��IM��$Y�9��\ �}��/�DěD��[n��m}��PRlWކ�B��w�S���w��aN�	�b���� �8
���"�9�2�%[�;����{���ls�2��r":23�a勤ьL�",�m�����S��i��M���k�s`3\ABǋ�I�<$3����	�J�)�yG�"������HiC()��ӣbN�E,��I�b=2��I�҅n����C��&�����k�hq��]۷ڞg�D��As��u�tZ��/Vc��Q8Q�Рas˺]HS�n�b����i�f8�����y��	v�A��O�()���x����-t��.����ܑ[�8�Qŏ	��'x�iJ*�Z�XS+o�nJ|�����D�*ӧ$�Ȧ"��1x/:%�N�kZ#��a�%h;w���Cۄs�}(%�$�1��6��q�g��8�4*��Y�
��>����m��.; iGoO��a�� �N�47�4�V�@� ��4��<??�� ,�`������ã��D�ߡ��t IG�8�U}*=W�$��`��!�شa=N���������쳻��!������$��$�,�yV��MiC�`��<�����NS�'Ƕ�%3<Ζ�}�A6ͼ:��i���#)�h?���ߴ"��ɏ�A�D���@���ػ�?~�����i���t)��Ho�C�$�Og��e\Y�!.p�+(�@�zH���C^0N��<�]�ȼ2=�p�������{�\!ސ��Y���R8���;4�/8���>��w�W�=X��Ax�lC��<��1l$쑨(�!�F	i��?�o�>&�K�(1#s�m�W�\�&H����C�".�sz��{UɈ��VD@�]��u}DL�$����It^�&���X %.�tE�cy�*^�2vM�Z���Glt��ݤ���RC)���Z�e�|�屳�{I�R�1|�
��I�����R
��$#!0*��<���`��ObzI$\b�X��b����:5����\1���� ��v8��z�-���Ej{�j?.��mO>��=��،���۷�:�"�C'�#rh��zp�a��<,�=G��֮]��ۚ5�ln�mkﰥ���,GNd8��a�?JE$����x��/��$��C>옣W�o��mv�?~�zc��zؘ�n�Zq:sE1o�6�ZL.]RE�1!hQ~�{���9� 3*�����0���Xo/��8ч��B(�&0d܀�p�k�ҙF\�F�ūH@<���+�����U����䰧��5H��>�v����h�2D�w~���AIR�u�a0ͬgԧ�	�}��;|��zzy`�2���Qi3����u�-mo���!�ib��J���� \v�7���Y�teІYNd����}����;mǳ��Z.ml�F0�CXu@��Fph
'���A��E��8���'%�(Uݎ�G�Y[�زZ������c?��c��1g]12~��/�y:=1-�@���� �K��ș�)�r��+1G� ظK����l&�KǑ��*��f�|LB���fK��Vt���C��v35�����R������x1�Al�1����=�g_A������2H��'��5� ���`ZY�@��y��v�/o���v��m�qD�%�d�'�@�QJ�ñ�NL9%�4��-�O�d��n���8�a��De.�9�����_jK��aPf0d(�AZ<�3�a��61>ƙV%�b�� /{�E��[n��n�|������*�x�D�)�.}	�R@���T#//|��&LI�W8���3v�/n��7?�iWW�>� ��v 3ڔ��F0� �.hAyvB"�w(�g/x����p�%G�0�(!��1}1�$���a)�[����ԫ%�P�ݹ���R�!���`C]�4�9��k���6��ݿ�gp{5�޾^gxP� � ���1g�)yk���a�1G۩��j�{����н�1�� �?�Wy�*�b�Y���m�U��Xf����{~�>���a<��2�2-p�@+B��'Ie;�Do�c��_|�S>�����X���9Nf�y�� Bf�����:NI�ø��Ȥ-նmO�G>�Qgz�'� ��<�Gy���N�ɉM��~c��g���8��z{���f�
;�#���e�F���٢��߀�r^�ؘ�Q3
�K	�I@���$�� ��f7I��%ל�x�w�#[�SNƹ�D���{[À�H4�� ������o�믿~qfR�'Ό�� %�lr�͙�dB�< B��8�����p6�F���H `�G9�=��A����_�b�Ħֳ�o�\��%K@ r'̠y1G�*v�����ɤTQ�v�03A��#�������{`
T8���zN&��TI����M2���t�-HX�dy����o۶lٌә���]8kK0�-|�ҍ���B��� �lΰo{�)�~�k��ʫm��e��w�ǣ����;-�K�����	R��(֣�l��)/�eh�#��:H8X?FRI�I[#_\b�0�Db��n{��k��6��/0�Ͻ�P4���[����Cv�����ر���~��7���{�+^i�y�+q�j?6�� �4�PyC��_��å�aIˀ�'�(F��:�Ev�'x�hl��N��ǡ�d���'�!�rɐ?�7H{�D�c�cy��E���y]��Ȣ�:��nj ����!�O�q#x�⥦z�!}�����IGȃT	1%,���|*Ռ���xA �"��h�Ic.GGͳ}�fR�"�nT�� y�7�I'������M26��:���]������¯l��-���g':H��9��r��f� ��(䒇@�'}�0I o�$���6���8D���B��_��x�٭�ѽ���mӦ���. ��[��ٗ~��M�V*.'0�����x:������/Y`�Ē��\~9�c��`����*�WE&iúAf�� �xv�]{�uv�m����4� KN�6b��+��ѫ˘˔��Rd��C6�W�� �l'�/|��v��k�e�\b�}�kQ�|7��A]m�z$��d�~Z�׵Q�{$��(R�,z�?�i���{��/���-�>�%Y8j���8���*��9��g޹��i�ҫ����p�X3�9nH3q�5�؏~�#;���Mo����0�A��%aަ<A�(? j#Wq-?ӱ߽���{�E}R�P.�7�Vq㽷+�l�C�hzuDI�/�[��_89����0S��BW-�R�{��K�����v0�P���I��I*V��j5�I��j0q��j9��L;�,�5,[��,#6D�^��1u�z�!��dsNq@��+���ύ7�����wc�@ِ�!���{��߱o}�[ A�@�?�D�.�G;��{8E��z��	�d\�
�KJ��:��n����/�!�[�!X� ��#`hyd3fz���O��Ӟ���� ��f�\�����!^��2��YK���s�>î�r�/;!����h���D�ʳE	��as���������uayˈ��A��em�g�����!�*�P^�!�a��'�x�������]o����1���2r��[�
�G�+�iț�JW:�]�C���d�6o~�>�ٿ�'�mCrI�C����x���A�zN�K����	a���^� �>�������~�ӟ�~�ڹ�P��g���O���A���(���m�a�q#$��w����˦��'ꊘ���K~��
��cMf�[k nt��>�<¢�m��6p?�!�r܍��}8,W/S������0J�s�*����>>G�2��`��y��N[�z=��-��Y�O<��)�����<�b�����ۼ�%�Dӕ����_�-7s�����睛l�d&����_�G���sf��`��s;��v�a#����G��E]��-������
��W�bw`)hd�9 �P��.�C"|q�Ps��og�I��<���:��¦���/!b�W�=fjn��k.s�td��=�R�E�y�@�3ߞ2�kq0��1E��h�7��r��=���ỳpi��)���'�8�Az��^��K�6�L,a$�BYsC,d����g�_��}Le��\v{�i8�*�l�%Iq�lKb*���{/|���u�-����$n��f������ax�+Ef�Z4���IWsv;�1*�=�)�tCf�+��/]�U���ܰ>G���I��^�'�
OL%���B������g��%���O7�|$�����bZ��T�n�e���,�#'J�P>	�(�-_a?��ϐ]㍞��;a�D�#L�^D2�P�����K.�uG�q_�?è�<�)e��޹k�K��g�᯾4x1�t��}��籡$��4�h���i\܆٦�8� ��^�e����Li�����6vp0�eh?ܓЈu���}�}���n��6{��g|ݥg�G̪�^�|��&!��Q���-�Fw�4-\q���?�fN��g��3�����)M,= ��G��,jv�෼�7 ���-�'�x['(��x�g�O��p�SH�@���b]��������q��Kn� �X��p·0�L@УNAC=�L����s������g�^{�/��K�YX�S�#1!uD\�T&/N��O��˝��皊#/��ޅ�Y$�@���]z�A]��7�O�^�]��X����_~�Z�r~|jss���2aYԧBBp<=��m��e�.
���D]ElB٧C�����0}I�8�jd�������1'��Q�#W�q?��[;�#6��$"��͎��c9:4t$\K�N5�Mb\
J��v�`|��4���9��%9�Vz����*{��|�������I���cq��B<�d^�p*�#������c��L�(�,�up*����H4�䟗]|�СL�	�f$3���@���l\�����g�Y��N�!�*1C��u��h��9!�x�̉�������c���P�����\�=��stS�=�T�n�yn�n��g�L�q<�lp6@I��E���|�7"�2m$�(��|m{{�����ccy�55�;F⒧Q�fɍ�,߂-��#'�x<ૌ{��#cPT���b�'Ԅ�%�{,1���T�G������a>��0Jy&��D-Z���(2���tڊS����"�A`bu�gd9�� �G��LZ��D��,qc"7�&ln%aV�*��u=�lt[ϻ���^�Yr[�>��i.�Ӡ��y��i(^��,���rK2�{� ������ ��QO�f���l�Q�kv�}�'?�)_r�ls�� en�%��Ч/`�b��	����-��1!A̓����u����_��8x�3q�D�r�PQ�����4���0�r$��jČ��}�S��v$dS�  �� 2���N�!?!����cNW��O -d`��7�Į��Z����,ғ*Oӈ?����}H/%%g�yF�Uc=b�c�Hᕮ?�/˼�Cw��s�8�t�����������^�3$�~W�8
� � �N���m3$JƬC ���p�#A1N �6�P���3���͗,`�v#����H�T��	D+.�O�z(��Z��̢����R:�>��p�������+ϥ&,�An�H+�PU-H�T��5k��Z<�GZ����hX�%$��y�Y���IC7��(��|r#J���t���(o��*��Y7)���\+�`I8��b���=������w)�_���8+��P����z�a'�T&�[���ǲ"��
;��>B:������k b0��h�����a�����V=�DݹR%��?��v`Ip�e�T�n���G�C��}Ɩ\�*ub��^vHT��{ٸO������Б]M�����������	�d[l٪M���A\R�����IS�c7U�RA U)0���$JBmW�NӰ.��
j�<�P �6�4q	 ߅O�aV�gIS�i��K�)�2o0(���Rێm��c<�n��hUY��!�pFz���� ?g�É<?��OIs��c�xV=��>�,2~Ђ��)��Ou���c`<Ť�%~��Y�BV<�C� "�;����W���	�\�ǭ�$��p���S�n F/�Tɧ�L��u�u��f�,�j+N��o����(N��X=0wu�0C�b��m@1� �b�dRȘ\s�w�<�_2�z�|q�ߔ���/�`�z����m=O:������5^N��~��d���F9� \��<�'J��-1RO&���ʅ/9y��J�b�%�I��$��g��)�P�3�Ą���ʛ�YB�!�@�7~����@��Uۓ\"���[\2C�N��afG��ܴ`�5�v�;b�� w����/����j�����UN�L4�I�Gꙭy��)%a�4jƨ����F��(ʬ��J�	Zΐ_u����!,3
�*���\e�+?b�1�%`#��\�v&6`�LH�����^���R�o�G��ܼ]{�u�����Lf�K����I�&I�b��2&yϻC~����;x1��\�9��F��r-L�Pd��;����#�Ǳ�_�}�q�tND�NHS9a=R���@���c��[�@y!�6,Ub�B��GVJ�'T�9�m�����~��4����V�)�@g����̑�~�0Z˜_H(���@����:?���щ.Qb��RU�I \A�B�4��r){ Pu6�T��l#��M����I�5Qpٗl����w�}�C'�Ap�U�� ��a�F���R�5֠f�{�m�򓑐/�$Q�>��]�S� ��F�bTZt
s�˗P�{pQ�W|���_Ji|[��1��k 4�(�k�� ���=852�S��Q�nS"r�W�=>'D�"(۸q���^�L�se��=�(��ٕn�v�#e��b��`S4O���G2��G
''��1��0�4͠��6��ќ�]t�w���.�?|�w<�}J ���"H�2$ ��>˕�1���6?�l�3� g��癑W21�-��i��w�c;v�J��˶�,%'�0�Q�zn�~��M7Y7����82XEoӨ�RC۶'���7�L%E�cJ�(2T�3��֭�����It~ǎ9t�a`bg�^+�@��Os�"\��VdH�q�_5e�s˺ȪH"�i���K	㹭�ᓴg':��W�T-�
'�?�_����p�]O7�H�菔R� �����f�W��֖fV�z}�xw�°o��k769�1���n&(�����c�|��ߘ�Ӊ�%<�����^~���`��'12�	��'�0��Q)���!u����m�MH�W_Y�j�2�-�X���.̄<*s���r���47��0$Q֌N��(�vGơ�u�5���[pq`�(17O�V�ǂ��х��cI��rK����u `F��M�l��ǉ��`�e�<]�D�!�y���{h�cƢ"�A3���P���t��*7��x��u��>n������������r�j �3X:4d������U<e��K��۶CJ�3���R�qgf��c9mǥp۞x"���67:*a?C����q�����<����>S�~���v�#0��w����o�M�$��;�/3"3+��6UI�h�Ri��;�El���m�n{�����9��i�m7�{`�=�Y�������d	� HB�*-�*�*�^�������w#^FFfFDf�{��U�o��w��w�ﮒoQ	�V��Ѩ-@���J�`G����.��P�Ï�����EZ��<k����Y���å/���x�t��
Cهi_�Q��s����اݺ^`�įGw�E�^�/�t�=��-���w�wo	5���v�83<��iZ�~=�S����yv�S>��$�E����@�LH,�!��} �\l�9|6��J�C����ME7����?��
�dվ�����������9�� y�=3������C?I�k9�^��L-"�c����Ø�n,$�5�[�@.����~��.�uJ�f��
>Vã��Mi-��8��5���l]䥠�@MY]��z&Qi
u2�+j�},�N��Ut�����Ec�z�G7E��%p�u|`G���i��?ܨ���Z�
�ƍ^}l��+D�n�<G 2��+W"���A�*����;v���O�=�9ϐ�N�sr���S�� ZG���&р��J�ߊ(>�N�>e?�������k%��t�w!.��w�Gv�r���Azh�����V�Z�\�@D�ɇC�̓��y���\!��j��gb�e�J�t�ͮ�F�솮�@{XH.PA���ȯko�K��؅�\�D�%綇�<�fW�LXS'�S(S�r{ {NsI����ǌ��8�>j�+Pb��[U�6H�H#��-(=���Ç�k��Qu���x���疆U�v<��;~��6����fk���IkRLI��0�T>f���4�́���.gݫ�u7�Sh�hݺu�ek���~0�!��]�h�@R�z+-����/�^��*��Z�c�[m"�GK�ppe��~�����T*�6�b���i�֯��<g�?ˆ��md�������e˭���'&�O���<~�8V >d��G����w�>�,6T1���A3�P��S�=hǨç%*@�?1Q�,t���$'_-�_�I���e�o�$<�u�k�k�}�ޫ��F�S^V���2�����ɓ����}����{��þnb�w#J�V�����Y��- �AޭZ��M�7��B�&�$ �a� �	~���1|��,������9��K"�9���H��EW�![�������YW]e�\u���v%�V1�}8ws>y=]�@�y���F������1P�ٽ�)�����?|���j�cJ�S�,�e4 ,j@n�!�I���y��-k�pp��-"�li�=2m���=� ���0DQq����ByF*��Ӱd������M�X-b��2fYJ��K|R����xرcǱ��A�r�f�;�pٲQ���NÑ?h$ á���� Zh�M���T(
C6�jf.YaN��k3��7X�i�$��8�62�PY[�ͭ���Dמ6�$&
54�T���>��RBt�b��FW^aW_u5�k<׶���^�����!����ሆA�#���M��-q���L�����y�n��F{�[n�''l׮]�}�N{�����o�>�.�<q/W4v�/�r�F�����ƾIɷ��IZ�(Ǭ{��.(#����Ul05��9�KX1�!�ާ�����I�Y5�6n٧�'�@~rf�*V�f���G�ډ�l��Aϧ�mf4[X����|�b���|֦l�l��\��Z� ��ĕ��Q9�����<k=߆���q�*x��Q��=�_�c�K�D�U2Z%%w���M��E�gn~nN�w������0�)L��L���1DD`�B�<�w�'����de����6�n?A1d:9���1�޹Z.�&�+��w�ڻa4\�F�	��I�\����t��0��+��y8wV��ӥ_��6{��_���f߾�N��'?i;v�D�0���� m�fz�Øw{��Nj&���J�C��� ���㒦��N�n�F�i �A�b91Q�#G��<|�S��'m!�(7�.0�:hkW��cvUj7�.s�ɸ���)J2����Bd�%(�2��w�����d�ų+Ũ	���}`��!�c�3mS���H�E ! �A�B�|�����Oɗ��1k�/zt�j+����[�c��Q	�2��z�A��M�l�ҷ�0gs
�i��s��
�Y�s��`0q�c
 #[.��2{��g/��������i�rV3SП��t)m��#�t�l{�K^ ��c>���~�������$�����I�������f���.�<+������LzE�<��d�ȃڅ[�烊���kʱ�{v�v�|N����w��"��{��;���Y�����g��D`!�pX�}F0�1B���ܰPG��a۰y+>TC�׹j����^E��(��NR���ze��Oq-*WеQS��ܼy�����k�u��-���5J��[*Q)��Y#��ʹ����R�Y�V�g_{�N]a��s?k�����_�G�}�k���$����A���Y�����ݾ���|����S'O�L���j���SNg��4U���.||�r�1��e�{��Jv����w~�a������� �w ��|/��kl����Tć��M����D� D`NA����Ԝ�s���&(���l�+`?�*�m\`7�����W�� �U<L�H@-q���hh��O�8�y����qM���P�Z���5����k��W�ܾ��/�wn���<=�ʔ��A���t`:v���œ'1+�����Aq�;_tL��V7�=���`�D�y�'�������O�n5��������0k�t3K2����qG��k@Q�SAٰy��Gq^�m
C0(�� ����%�9*|�Ht�E�7(���wԬ��	���>��"���~���7�O��ͶiÙ��JyR��
{W�Q���*b5�eV);�Ï<]��B�̡�0�L�H�q٥م����K^r�����ۿ� 21��	B����Tt._��G2FB�4��~o�sB���/7,�0�/��ÁO
����� '�v-���֒�n���L�c�:߀��	�p��G�s ����jpp�&ЯtŪu0������X�6����S�"�&�,V/iCt<d�'��L6�hl
���q�E��m9�<��w��=�y����J��aP �a����4\�ۋ�'e�y{"��đႽ�������¾����c�`2���"&!�Q%y������]t�c�S����Ri���?/|���ԌR/������4�A�P�F	�y�>%�)'�T^E d8�1� �0|	�%�e�۰¶]|9Ԁb�ZN��ˣ̛���̝A�IZ�i�9����ш)���U�z�����<�L(�i�a݉��W��c��GE���2k`׬^a��=�f�{�s����~L���-�R�:�.O" "�)���?چ�cǡ�,C�Aۼ�l[>���:pK���"����b�x۬�l*iV�)�&]��'BW�Y#˗�O��-��w���A���s�òh*{�/�(K��Է���q[�l�^��ع�c����]qN OQ=Ao�D@D@���EŽ�"�b�3�/��[��6���ˈ�S�?/�}�G�=Q�%�d���`��qΎR잴~�z������e/����7F���S
�_�F�(P��������SI2���=������r��m	/U&�n������t����`�@Qxs
�!�}�5ϵ��j�<��5�azV�P`83�}�E����U�hq�cc�	����^|��k!s�����gW�mQ����>^�9��q�#��_J�&��7�Z�Bw�(��a�����_��0��=��?" " �F@�C7PO���a�ȋE���Κ�PL&7�=����<z����m����O�O���a�l9@�T`4� qHt�Z���*۲�r�E�s��1�*����-}i��$��am�3޾1���  @ IDATXq�X�2�Չ�pL�gܰ�,������/|.��Ѓ�a]���)�4����
xP�]A�a7�7%d���i���|��i�l�6���;�p�o�Q����j�<�X��>�R+z�]Z��S�<���y�] 
=gf�ʙ��'�q�H�����f/|r��q�nF�S�����ln�$�Z\�o}�َX�p:�8�QH���~�%wm�u(,�Q;g��n��V���
W�f����&��5�:�����aA����b�x��VWd�n�a� �`�c�sjƑ�!{;A_���*��IQ����S��/�g�9ҨN�G���xJ�;?���_��ˑ\�H�GSA�>�=� Gs臨x����q���X��3h����(S�%}�����B�X��l����x/u)W��VI�!)�S�0]�^(O��+"��8t@���?B�ŏ���-�^�u��{��
S�LEDO
�@������6��@c�T��Ȳ�v�y����lA_c��P�E�|�U����ڋ�"-󋌯u�[������D	�0�1�����~�-��W�����Z��"_��e�w;1�q���\�ǻ̵�f�:�4T�&[��/�ȟDE.>���e���OS/s@ssя,[f�GG}`3�j�:�i�qq�� �lN����j�'���Z�j
d�9T�[�)�Ѩ�P�h)�g��
�<���őe��+쌳6����p(A���J1ʹ`���E��t�p�z'���]���a�.������~�]o�����a}�Z�
A7ܣ���@�o�+�A#��H`6�����?��|�!���v۵k�>z�;M�8Vs���@��S�Ҡp�ߍ N;y�6<<l+��l�k삭[�ҋ/��.��V�-�*�o�u ��A��1������䑀�r�]wB����r��^m��QsN��Px�cz��m���Z1:�}�q���>��t�GŢZ����ZW�ʕ��=	a0h�*`¹����!�w:T��b�.6��}�1����7l��P�1Kk�+�ɧ�p���g~��6�5hH�&aLpe����y�QA���Mb���َ��]w�ew�}��۷��g�D�ř2~�,&�>�ী�~5آ�V�8��|�!H˶/���g�\}�mڴ�V�X�4N���<e�)" "�M2:��}�1 �5�aÁAKa��R4ެ��]���紐;���2�x/��6��]��n�}�!PE���e���v���mxd˺�{$��L��{��͛9�8x�!��0��_�!�wQ�
,sv��w�Uh�?��Kﰭl�Ή���;�ߙ����q҆�+����$Z��[��wn�7۾�Q,���[V��/��F�2 z�,�����������(��Tf���c��0~x�!�-C��H��_f�y��m��-�M���P�?�5��I��{:XT2:��>(�2��Q {��g��J[:�Ҷ�X�d�"��|)�*�)�����c�*+öz�z�v��vu�Ԍz
�~�1#�(4��k��"�m|��[t��i;���_��I��L�n�. s	�D�E�_�q/�EΠ�׶N�Lј��#��I�+{
�w�e�ѿ�}����a�V�E-���e&����.�7���F=��-��	����q{������|�������~�]�l��X�1������+h4iȞ��6��gB��(�lcｂQȹ"�=��Ӎ�Pd�Z|������1�����N���A�ŀ��E�
pl=	���k6�r���n��Zs����n60�p0�� ��`�
t(�3Q���a��D@����]����ʕc�3o}s�<�i{W�.r@2[�|sl�߽۾������>�,p��7��/k��#߭ƛ��̽�1`)wI<��n��8��X�o��?�]�������[��S�f�j|�E&��W*����dA@�C��Y�h�o<a���$(�(>QCs�E!��f�w�(K����q��C\I�V�@p!�B���/�3֟egb���Ȩ��hq(b�Q8�jᠳ�wOb���0ԩ�D�g�3��@�	иNޒ *ϻ����R�����J�袋��O�4�xYy���a��O~�����}�N�:�݇
�\��t�+3E�w߉$B��L���+0�_	ݳ8��r���#=}�>����׿�M��?�cۺ��$���cѹ���@�	�ph�1k��߀������LC�C�6�|%
��d������X�9%���!�L��H���q0�b�
̀2��&/�QȲF	�H"6��� U����_��c:��J8t�erA;X$�5'y&;�����Q�U��:���O������~�[0�i�Z����f�/��>��?h��G�����M��a�/&�+��x��46��h���F-z48�������yB@�])�h����yj��?��߷���W�%/yq�����vaƨuCD@D`	�ph&��P��}�ܭ[���m +&�0��1L�ڨM�C�XҥK������{���q3����#�2��wf���쩌`@#�񇩓PpCE��e�\em$㄂���h�G{Yώμ=mc������>��ޒ0h9tq����1�,����0�?�h)�����}��K����y�����
���FՓ�_��o�!���A[�f��okG�0��o�=r� �5w߁�g�۱���M����6b�S�n��Д*O��R��
(�����
Gl��u��m��QW��Դ�3/�2����;���_��B����8��M�����KP�]&^p�1S�)ahLpZH���ΥX� ~��YR���Dz�(���e�@F��i�|��h�ݘoH�IP���X�����6��B�zr�~My�(ɔI�Q�p�g�O�����G�����-�Lz���|�>N���E�h40^o�D����I����NO��?�Iۼ�l{�+�J���W�����t�@��~\���h֢C�d�^�}@�fL�uX%�4�r���gٲ��Xˀ�{`LpzR8`�[a!��\S�N~e\�q�zr����p�F����{i�qp�h�p����V�� �g+��)A:���	��
�Q	a�`Pb�X1��3;ލ�ڋ�����l>۝lQy�w�U��0Z�3��B7l�+��4y3����)a�F��j���k���UX��ӟ��}��D�!��.I�#��7�Ƃ�������z�_k[�V��#�|�	�����(��{��z�������=��w�x�o�6��% �!��B��Բ��gֺ{i6���/���A^����7l�*�X�"у��?�ĸ�1E�����<�K�~7;
���>��]h��lժ1�i��lR�;����8��>b��zk-�e,"Ge����9�����{j�}��à�q����e�(̭�LD@�$Ӳ5�>�Pr%5k��k��nJ�m�ؖ��a�!��[�L��T#dZD� "�e�\&��]��rn�p+&)�X)Z�h�t�����E��a���g�����`��E�=����6���s����@n.�����0�K^�)����Ă3L,�Y>����
�|�Ь�C%��WJM�C�%D v��V���_v�en4�Vvl/�Н
�-X��s��ۿ݉锇}2k�9�+���2�ړn~��d�}�7�8ƃ��s��=���[D@D�U2j�B)���.�Z4V�Z�9�ê�\8���%b �~��O/���NE@z�@��$v��K£r��[����T�9� ��v6��j��ɒ��� �h)�B�c4h4t�jG�Vݲr���������c5z1��W�D@D �d8$9Ӵ��,�9-��(H���ӱ���[5�קAr��R" ͛���հ�w�c�|û?�qNCЭm���X�}u�X�-��t̔��U� �=�ē�s��$�p�X 4,�q:�^8&N]B��n���p�`�B$���,�+	{P,�9���x!=P�	�`�Xh�q����.}O�" �@�ov7n~%�n��Ӓ�6	
>�������޳�=
�\k�7�?���e�ł/�y�}���	o���Б����b�����)	k�Yo�������*�XZ���������]g=Yj�R��uџ��.C�0��������UNͽ�jד�wl����w��B�Ø�Wo��N�q�Ҝ^�+\�8y�v�ލf�<�.�D@D`i�pI��|b!˽r���Ă,�T^ ׮-�D���������1�H{)|r���\k%buǮ'w��l�῕8�rS)���}�0%�i{��g��*3��@_P�M�����}!^�������!���"܏O���6^�^D`Q	�ʾVm�A�S��0弃�f�j���]7 \�oO���̧`-s����&D�
�׀��Q���JG�ə�GD@����瀁��@J9�r@$�ª�
���yKbz���JvK�Ȟ�&��@o�)��^�i�����րi,ЅU�V!� �(�
�AS#�*˼s��I��j�ܚ��[=��>�����3�Ulb���/���PFHT��'��J�#0P�$I-�z�Ak6��(�a8x�NCb֒݋�9����' "�5�QO��5�Q��l��$��x�9v���	(�AR|f��~�9����ӱrV&�ZM�L�<��8|;��G~o���J�m�+�#
y�@�g�!��7T,}}�Ĳ��j�L;����w�-�����H��fJw�ٚJ���8ᛅ����J�ȱ���w�i����6�a�tRͳ��)4�Y	�p��n���;���}��qo��o��1�MÁ�(��5����B�� � @��r���]��6:�lJ�N���4" "�t	�pX�y���@���+z������6�rc�U�[~�:�L�������f]<�v4ފ(�rl%FthXl2���X<`9Po_�o=����o�J�I$���T���!r^mj �\ay�-�wW~[�*C�DJ����H㊱1۸ᬞ1
S�С���<=��J��@3�ނ�.?mjщ��0�U����O>i�'kɈ���Z,��w��6<<��\�rilq�}�]��6l����H�R!" �C@�C��$h������
> �a�����	E�
��o���{�+�ǬJ��o�6�~Й�@K
�8%+���zc���>��\�\D@������s�XD�4�U��[~����g3�<�l'���LJ����v�UW��V���6fTJR<�l����7Xa ��W�&" "��d8,*nE&"��b7����V��6���[�֢�r�d?����Q-4Ls�J���o{��lt�h7En1e�;������Vv�z��_e�Wc�m׺sEGڋ���t����#V" �N��J*�߾}�,�vTa��Ԧ)'��S,�&�0�a��x��8���8i������}�k���E+K��������0w�#Y��6�It�
�V��"��	p �bm�dd;}̞>|]��ԣA1n]wK�)"oz�k��7/V�ͥ���e/�K.�f�r�-I�\[��������07�2~��=(؃!�����D ��b�c�([��m��Dϩ`���v��AN�6�U)�taϯ�������J����p���?Βĵ�C�֒/��c���{�&{���F0~b ��g�-����i��'Wj}�b_��yI��{�0��μ�ô
SN�Ѥ��s��,{�;~�SX,Br��Bw�D@D@� Km5�(��@��^- ��dM 1(�7|��U��U��S�����A��ء��.���4��+^�R{���
C0�e��#�r	!N�+���ӿ���[Bj?�G�~�=eN쏖�,ZSBQ^ʲe���;��[�z�JgB�C�C�^������,  QA����|	��ѝ;��{�Ԧ��c~�h*௿������i	-� �1��`��p^o�kLa37ͮ5�krNo�(�68�
�go�l��[�i7m7�	����&" �O`~���˫E@�$�has�[�j�n�8��Q��nD7�|3��k��}�i$�.�����f���n�#C6��,�&���#��PW�CKC��-����t_�&���ݙ`<�kR�R�+�������͞u��h��}ȁ_�8؍��X�LD@D@�E@�˺EV�����T�7���,�����KL��7��w�- �ɒ���G��/�5�T�B�A���ǖ�؛�x�m8�,��G��v�~5�!N���;��X�����<�����[aϾ�tO�m�z��7�8����|�Zʈ�\X)[��������0k�I�x��E-.�� �&y#@�Z"�O�eP�P��^���q��*j���<�K牰��AW`���^�_����M_��]r��cM"���9깍-m������k[���V��ۗ��;~�?0>����Wh.$�0)p�&�@���^O�9n�+T0}Bs�_����_`�#��D���.���=ZG�{�sB��?� �x(^��60�OUE@D@���9(���-)ca8�7��E'���\M�
g�q����+������¿�[0�অPӣ�#0�護~�^�נ��jW�?�k*�A�o_i�倝����#�W��?����{���I�������h`� X�x�*���	B־�x��(�E~9�5����� ��-4�b��0s�a݉e��l��X��g�5�zV�N�v[�<$�@�?�iXl2f#β��3��У�P��H�䒀�lC�{���'ϭ�8�'��|�2�� T��>�ri� �?�a��?�#;k���{�A��n[K��<�p����Z����g۾�Q��?�q����ک�']y��	�>�l�8�sC{� zNˍW�x�xL�?��pV��� �	-�n$��ƍ��뮳k`]}�՘5i����M06ϔg�J�C����@d8�A�kӼ��L�^�GelO�-(���A��xfY�[)C�
�]e%�������O���[��)c�q��w�BM�$�:<�����/����{ޅ40~�ӜR������-�a �{XD�m�f�\�����mr�j��~;Z<n��hA�lI�3��{�/�� ����*���΀�$Z-hJ(^x�e�_�|����/z���uo���?7ђY8�fa���	�U�W�1��ݦ�������9����dF@��l�Y@�@�
�����^ت���eE�ȑî�y+��}'
fV	X�xk:�1��v�#E��xip�A��"��Ri�l_��W��˯����:W���[���-	��U��\P�a�l�X�W��z{�K_%~��<��v?��<h��y�N�8mǎ�S㧭ž��M%�,@���3T��M�6�|�V��ap�*[�f�mB�¹�kk׬v�4"h�/L4�6���oΛn S�|�������������k�X�Q_�I�iDm��6P�@'��w���5�3% e2�V37�&�����\n��Q���a�t�m��lw�������)�t�EaL@��3�V*����}���Y�v��W ��x���ٙ�h�g���t>	D�4�lضm�b�.�/y� [�8��G�p�9��71�n�|���ȍ��r@t<���5�'tOb˂��Bt�m���&" sH�"s9��y�V���A|U/�P�UB��2J1�ԣ�o�N>�ת���{R�����{X(q�B���Fm"�)>C��9�Ha�)�x�&�]�ؕc`�b'�=cǏ<%��T���AqÙGM�0����E�k�A#(�3��3\�'*�\R�
q7��2�s�v�ĩR��`Ղ>r�>�W�'v?�o�!=\砂�.�=��w�Sdf�'�7,��*�X�-�y��%��dS�.b19�*���rl^�օ˗�1��eX+�Çv@����q����0�t7,�2����L>����(��6�%E�釫��?T������jp�%�]u��
����Y�����ĸ=�Y�4nC,y��bM4جN�{/Q(���J��`�wY���t��jP����ǵ��!P���L��=O��z�j�X.�7q^I�}����C�6(�1���Kמ����j)���O�����jO�x(MҒ᧛Jv�����B3��in�p�Z�B4��h���K_�wW�zf�D��	ď��.Z�������j��pm�ed?���g�N�O�L(Y�Z�a��C�_(š�P�:�=k�B������3�f�� Ѥ��� �;�.T'O��}O�����HeK[W�@[���1�s۹�1��>۳�)z���(�>�t�����3�Ǐ���|����/���S�MD@D`�h��,���P�>n���ɝ(�����a��QT��	=iY�]C���;��6�Z�ΰ҅c�<}���<�����z�<}���5g1�h&O��ٽ�dm涓pr�椺�]n8f�;t��8��T��#v�;q>�����-���?������S���K���4�Y���y_�����������������\�o1�4�1{V��_I��T7D�ӲO=;q�}�#c����ت�k�L���MD`�HW��ҷl��GH��Y�}������69~�cG���/�ĆGW����1�7��Cq��9';#�z�,�QI��c���|�{��,��p���++��1=��y7��8��l�s����e����3D�g��mN��۳�Q;t�)�JS�e�WZ.;���SB n8�*�C�y�Q_E�S��i磏���?����ߵ�>���h�*t��c�|(z����dG����|�c�7�_��}o|o��;O�B�^$��W���o���<��9r�����Հ�P�N������ԃc��m�p~�-+� �[<��E<�M�s��O�s�1���aҋ�Ji��1�1�fq��)�x��pf���pb:Z����2�)ָ�G�P��Ѥ���~SdN����SǬR��!� [@F�Z�ܵ���0��̅�6�;�`�;���ډ��06ƋV�h���B%��#G�����ox���g�֯_����񙒢\�j���t�i���(O��A�J"_�J���C������GBXQd#"��S�"��}M>��`���X��ٽ�oh����SnZ% áR��Ň�6��#��@�>}l��R�Z��g`B��?t��ݕ��~����w�P �6�����x�p�HL�����G�pڗ��B�mY)i�4�&k�]�4#%Ӹ� +��\�8V� M%�gO"��\�ǒڭ6'���Z!�W�'��NW��o�1�Ů3���Jhʬ���������k�}�{����P�Aw�q�K	{<:T�C�Yc��/�7��7D�,�������������N�8�T�=`Z�w��"ʤ��@�	� >Ƃ������+V8�>�ԇ8�B3�i[82�a�(�A��\P�C �6�����8}�t����������Lu;۽��q����|}k�y^+ݣ��w6yf��gs�1��e���,���9�� ��z�.e@{=�0��3�=	P��=�� q���&O�+�~�������[osd����'�@&tZrQ�l߱���K�loz���7��6m���a�Rq��h�̀`+.gG"g��顬��/��e��?�������~LÀ�����s� P�1����oy��њ��R,z3�/���*U>��EW2Z�v�[>��pO�o�6�	�A�K_O3���;��n����o��X�pzI�V�LC?<g����8�+�|��3���@ ��d��i��|��g���c�<��q(:kF"ܱ�R+,W0�� Z*�����	��M_��o�/��_�:��>���0;S4|���nI�p�A1��%��3�Mr�-ߴ������cǬ��'��Z0,nq��WD��	p,7���E$ceA�)���[Xiµp�;��VC��V�ph�Ҍn�`,Y����Q��&�Fg0Fxަ�����Xf,���&,HH-¼�Y�2�*q16�Dm݉���������� ���=�6o��qr���{w��X8gLK�^�c����ر���#��W�z�}�;m�4�B�-���a�C���iQ�/Q����|3��_��g�v��d�?���8[8#]ah؏�#���j�G2: 8��c�X�	fq��p�����=D&/}K T�B��?^�S>uAw��itW������J��-_��3w�|�D]����ށ�l��������#���_gW_y���Mo��/�ԓ@[�{�U�ɣl�el'�&����x������md�;q�c�Lp@�!#A�����a4�&�R��R�O�81�B�.�u���}�"3��ȹD�Q^��c
�>O��Į��u?��j��'�����&�'.��Y����=����x/��8z�S��>��m�ƴ���cn�M�^�
?~�!TL$�8�\�nɇ���x"��Z���"�|��ܽ'�	lU��?�0�	��B������b|]�o��&��p��v���5�F�5��C^I_�k\��B#�n�.��/)��`�b9�u�k�`p�|�;��B�BcH8g�tQBS��=�l��v�?}˶n���5W_n�֮��ccI���p����-���+�A���W+�q<u������ᭊ��ԩq;x�������7�l>��?�L����F�܀@��0���5i�ړ�x6�^������$����}Z^���o�W-�5v��36<2���ROMW�4r^'��G�c�9:�%�<���DC:YZA������i�R��%�Ƥ_S������_p���V��pn����<<�����{�s�Y�S�g$�X(tpuaJg�Eωh�l�[��`�}�o?�ALuC�<�����:�@^\����pK�" "л��w�ٛ��y��٦��DB�������*w��-�^�/�|������ުk�"j��W�t.l�b_r�=�Y�ڦ��^�R�A�}`5P�R��(��#��5��'O���;���~`?���������Ӈ��p��虌��V�[�q�&W�\Cvœ3_��kDLMr�}�q���06��P3��US�)Y77Ȇ͹���|!�A�p��Q�4]�43��s���#v���ZZ��ǒ�?d=�3UG��kVۊ�xn1'!��0+��8��f�g�P;�ۻ�)Op㳓3
���s�����|]�S,�����)r�g���/6?�1����W����$Yh���Rp����� �1R���(;;.3Q�v�7c�T@��q���lE�8|�(ց8f?��C6��[]�5P�.�����K��k��sϥ!�����?c��U�\�&��~�$S9�PE�+��O��o��}�}����Xx�N��!L��(����\����|��XQ!,�\L��?nEW��9o~�:�s}^�I�=�����.���*�{�A���CV�����!�k�:%�u�)���2v�����c��3�����n��5�Ս�
%<#h��� |�����K�o��;BK�x�1+Љ�'���S!��X�Y�ܖP��a�
���>#��l)9�C2�0ӕd�(=��:�4Ϥ��/�n���88 ���Nc_��O�f��A��	!=}���.��{߃b�)+@e���ի�[c���P�F|v&��D�~�'�}Q���	�|��a(~�=�CaawZ^���^��˄C��Z�+�P��r��g�+�I��+?��6���6���T�����u�1>��m-ԅq����8[5;(��:s��s��)*�4��5�E�c���bg*���igU>>��9�D�#�1e��.#�^�Q��n���� �gۍ��ih/%N�ő-�@0Bm"02�O^E@��������Si�`Ñ�e�7=�	�24�+�TPq��ɮB>#	��b0����Q�;`O��RS7�}
C��Ն5��GcT?�T�J6Tr���V(���ABC�S�R����xm)�p����!��6�rz�4*Q�gk���Jr!�"�]t�PrK���fw��r9ԲSO�5q��n�hHj��l$lZ�<wl�s~8Ƴ�sK,�#����d�ԩ�q����U�w��V;~�Vf! �a8�%"ЛX ����$�'[�p;��T�Hjr��<1�* ����:�C(��?���,y7�p�cWDx/	'���F��Jä�V�2#v�.(\��J!܂��S���g{X0l�OM�)Λ�@6Pp���P�=S|������ bM�)[����Lo�a��=O.��ci�8&��8��iq�ʷ��{7>r
�)��.'�.����t��"������8�zWg"�>�3��!���+e�L��m%����'U(��w��>( ���1E}�{8��'ټ;	Σ�x��*q����`0$�&���ocO��E�m*t4�j^�uwI	�x��Q�f^��"���]f�Ay�S���F�BK��
��y�yC��Lc��mp^S�xP)�����4���39N���69$��.�Ipډ@�d8t�NE@�����,��nܳ	gfHD-��7����Da�D�����A�`���B��E�3D���&�V�ư�p�m00���fxmQ�T=�Zy���ss�.s�'���@�:�V�>�i��% �aay*4��`S�lI%���E����M�����&}/�5^���!v���x�'��"6��5�
p�u��j����Ak�r{0-��N_n�2��q``��h��|��~$ ás]i�>!P���Izix$e�R4�G��2������:��I�̡,��͜��w�"0��φ�,&�I[q��,>����f�u�k�r�o�qt�y+�̨����f���
���@�i��s���V��`<� G�P@���xu�V�V�����G�N0u_Y��'ɛV2�,R�~�s<��r`�=Ϣ}z��}2��X1��,64Ĺ���z�A�>;�L�WN枅5�1Wݾߢ�t�fFB'6�� ���TtI�6�'n3�mD�8m+���_@so���y2��9���(�]#0Ǜڵx���t���2�Yt�ݕ�+bӯ�D��8CM2[h�E@D@D���p�<W�E`���ɴ�ɺam��Z��#[,f52�]D@D@D���p�<��" �@#�]�Fo��T7��5��u#b�������@����?y���@�`�$�6\,�r2�b��@+ ⊫t{�ԩV�ȍ����,i2�t�*q"П��@�P,�Ձǝr'�'��r�i��'" " �" �!_�!iD@� ������ h�zH,�`���?�d�*�=2z/�$����M�P,�؊622<��&�C�&��i]�;FH7q�K" " "�/d8�KN+�"�G�RP�tJ�W�����|����`s`���:�+���M@����_�N��@�b�z�*�DmtUJQ������O��:��# á�\	��O�®J�A������0������š���<��W�a2z8�$��:�4���)�l]���������=����ֆ��~���S�!yx��ĳ��>f'O��Y�a�B;�'2�)��V�Q�tv�di��B�J��_�p��m۶�6oޘ��:�9'+���F���ݻ��3=h/" " K�@q��O��1���VE�rυ�|04�'��U_�����{l�����-i�S��bW,a���-�#���<�;��K@-K7o�2XZhe4�8U� vSb�~�m���k�K/u�dd�[�z���?>n?���j��&" " �L��j�~&����,<�6���!jN��V��$�'��W�X)z�8h���?���n0P�gw&�KwE��S;��[�cO<��q7J*�nL5/:�>"��>�l%U����dm�s-C0���w�s�s-�;@��рA�E�m4����֋���8q�*8N�,��%W" " "���Z�.�T+5" � �b7��?�vn�č-q �� �IE%8	�Q�7[1:j�z�/�[���4<�1V!l�Q����b��b��e%t�����;��1[S�T��������}��J��@T��>*����-�Y��ŠR��@���� �624dg�q����=�ꊋ��# =����܍��s��d��P��ӧJv�}�Y���9 c'8ū6�W2�5�nȐ�
IM4܈���R�`gh�t=��*��h.T*%f#X��/��{���u��5kָ��4x+D�x�)���
� �D�>��/���	*�+��La�����,e2�r�*m"�c0��JM��4�f���vSb%��A��5�v�Z{��go��Mv�9��؊enH�^�˖2��}�j�����H�g�>���}�}����DCF���ډ����+���J�dH�F¦M���\��%tI*[��z~���k�#�C6<\�c+m�"m8�,���m���M>��#���T�P��X��`�T9{M��$���>��e��֯۩ӧ1�]� ۠wS�����ᐃL�"��	D��Ǘ]r�����]Ň���ً��E��2�0�����-�ON� jvk�X��E����7o���G��m߾���!v�
�t��"" " �@@�C?��(�nHIW�(� �
��vZ	-��0��S��|F�8�E��������ǟp�C�e�[gq$����& á��O@�����6=�t�Bw$.w��]��W����J�����,�W�" " "�ٱW�"�W�E)n<N�����7Q��쇄ٛ��w���'�?_��EM����J��E@D@D �d8�1W$������m0�Z���:�:=i��Gm��GaHplݧ,��P�"H�(D@D@D �8P���,q�VJ�	�28��_~�n��6�ƺ8�oS���1�ND@D@D���š�2[I�<��dV�wk�W�清86��5*̼D�>�>m��/�
9
nDT�EyzR$����@^�p�KNH�#@�!®�����p��?�s���܎�*�;��R��F!"��^D@D@�d8�)Ȇ��#�N�qm����f7�ݷ��}�㟲�n�7+�1P����Ԭ���CwdS�" " "Ыd8�j�In�qT��U	�shn4�\�%������_��_�޽�l||2�g`�&��:1�V��J��jup��#" " jq�3 "����C;���
t��o���o���v��q�b � �/����*V�f#���a��t�"" " K��Z�l�*a"�sP�]��.KQK���U�Cէ_��V�D��oa�iLLT�[�a_��Wm�Ν�.I�b�����0x�� �C�\��" " " 2���dD j퉡��l	���`<P�h,���( ��R�N�:i�����c��=��X�M	�����`�>�^Æ8j�f2`�[�E@D@D���p�WrE /|:VV�'����r��TYa4�kQh��O[���=z�~��v�����۞x�qw��3���U0@m" " " s��0'"9�*�eL`���������hA�"�=�y�F\�a�*�%�я�[n�-ߵ��0~aU�5���>��ij�D�E@D@D@f  �a0�,"�]�b4�s�  ?IDATY.�ʼw9b�!e\�,MZirc&0�ф9v̎9nG��g�9b�v����쳝�n��p���nU�C� �A,�VD�m�M�B�> 0p��nP���$�@��m�k],bN��T��qO#�T*�u����hP��N8B�g@b&h\(��l��!fG�I~�������tD@-a�'���(ٞ����/��f=�ݚز�P`(pO����N�u:�&" " "��q�/� ���Nm@B�V�0MRݘhӽ6���L�" " " ��jF���-��"�-�%����!����*	*K�@�a�iC8�с!MV��,�" " "`&�AO��@F|$B�q��HJc�f<pP4�dm���4��k" " " 3��0#��.��o��4$��+�B��" á��[���Xx�!$�[�����E$м-PT" " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s22�	 " " " " �' �!�y$	E@D@D@D@D s�?R��x�_�c    IEND�B`�                                                                                                                                                                                                            phjamf/jamf_connector.py                                                                            000640  000765  000024  00000032300 13647126427 016331  0                                                                                                    ustar 00smasud                          staff                           000000  000000                                                                                                                                                                         #!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------
# Phantom sample App Connector python file
# -----------------------------------------

# Python 3 Compatibility imports
from __future__ import print_function, unicode_literals

# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult

# Usage of the consts file is recommended
# from jamf_consts import *
import requests
import json
from bs4 import BeautifulSoup


class RetVal(tuple):

    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class JamfConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(JamfConnector, self).__init__()

        self._state = None

        # get the asset config
        config = self.get_config()

        # Variable to hold a base_url in case the app makes REST calls
        # Do note that the app json defines the asset config, so please
        # modify this as you deem fit.
        self._base_url = None

    def _process_empty_response(self, response, action_result):
        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(
            action_result.set_status(
                phantom.APP_ERROR, "Empty response and no information in the header"
            ), None
        )

    def _process_html_response(self, response, action_result):
        # An html response, treat it like an error
        status_code = response.status_code

        # Handle valid responses from tryitout.jamfcloud.com
        if (status_code == 200):
            return RetVal(phantom.APP_SUCCESS, response.text)

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            error_text = soup.text
            split_lines = error_text.split('\n')
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = '\n'.join(split_lines)
        except:
            error_text = "Cannot parse error details"

        message = "Status Code: {0}. Data from server:\n{1}\n".format(status_code, error_text)

        message = message.replace(u'{', '{{').replace(u'}', '}}')
        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_json_response(self, r, action_result):
        # Try a json parse
        try:
            resp_json = r.json()
        except Exception as e:
            return RetVal(
                action_result.set_status(
                    phantom.APP_ERROR, "Unable to parse JSON response. Error: {0}".format(str(e))
                ), None
            )

        # Please specify the status codes here
        if 200 <= r.status_code < 399:
            return RetVal(phantom.APP_SUCCESS, resp_json)

        # You should process the error returned in the json
        message = "Error from server. Status Code: {0} Data from server: {1}".format(
            r.status_code,
            r.text.replace(u'{', '{{').replace(u'}', '}}')
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, r, action_result):
        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, 'add_debug_data'):
            action_result.add_debug_data({'r_status_code': r.status_code})
            action_result.add_debug_data({'r_text': r.text})
            action_result.add_debug_data({'r_headers': r.headers})

        # Process each 'Content-Type' of response separately
        # Process a json response
        if 'text/plain;charset=UTF-8' in r.headers.get('Content-Type', ''):
            return self._process_json_response(r, action_result)

        # Process an HTML response, Do this no matter what the api talks.
        # There is a high chance of a PROXY in between phantom and the rest of
        # world, in case of errors, PROXY's return HTML, this function parses
        # the error and adds it to the action_result.
        if 'html' in r.headers.get('Content-Type', ''):
            return self._process_html_response(r, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not r.text:
            return self._process_empty_response(r, action_result)

        # everything else is actually an error at this point
        message = "Can't process response from server. Status Code: {0} Data from server: {1}".format(
            r.status_code,
            r.text.replace('{', '{{').replace('}', '}}')
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _make_rest_call(self, endpoint, action_result, method="get", **kwargs):
        # **kwargs can be any additional parameters that requests.request accepts

        config = self.get_config()

        resp_json = None
        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        try:
            request_func = getattr(requests, method)
        except AttributeError:
            return RetVal(
                action_result.set_status(phantom.APP_ERROR, "Invalid method: {0}".format(method)),
                resp_json
            )

        # Create a URL to connect to
        url = self._base_url + endpoint
        #url = "https://tryitout.jamfcloud.com/JSSResource"
        try:
            r = request_func(
                url,
                headers=headers,
                # auth=(username, password),  # basic authentication
                verify=config.get('verify_server_cert', False),
                **kwargs
            )
        except Exception as e:
            return RetVal(
                action_result.set_status(
                    phantom.APP_ERROR, "Error Connecting to server. Details: {0}".format(str(e))
                ), resp_json
            )

        return self._process_response(r, action_result)

    def _handle_test_connectivity(self, param):
        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # NOTE: test connectivity does _NOT_ take any parameters
        # i.e. the param dictionary passed to this handler will be empty.
        # Also typically it does not add any data into an action_result either.
        # The status and progress messages are more important.

        #self.save_progress("Connecting to endpoint /JSSResource")
        self.save_progress("Connecting to endpoint {}".format(self._base_url))
        # make rest call
        ret_val, response = self._make_rest_call(
            '/accounts', action_result, params=None
        )

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # for now the return is commented out, but after implementation, return from here
            self.save_progress("Test Connectivity Failed.")
            return action_result.get_status()

        # Return success
        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

        # For now return Error with a message, in case of success we don't set the message, but use the summary
        return action_result.set_status(phantom.APP_ERROR, "Action not yet implemented")

    def _handle_get_system_info(self, param):
        # Implement the handler here
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Access action parameters passed in the 'param' dictionary

        # Required values can be accessed directly
        #Syed changed from param['id'] to param.get()
        id = param.get('id')
        username = param.get('username')

        # Optional values should use the .get() function
        # optional_parameter = param.get('optional_parameter', 'default_value')

        # make rest call
        '''
        ret_val, response = self._make_rest_call(
            '/computermanagement/id/{id}/username/{username}',
            action_result,
            params=None,
            headers=None
        )
        '''
        #Syed changes
        #print ('/computermanagement/id/{0}/username/{1}'.format(id,username))
        ret_val, response = self._make_rest_call(
            #'/computermanagement/id/{0}/'.format(id),
            '/computermanagement/id/40',
            action_result
        )

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # for now the return is commented out, but after implementation, return from here
            # return action_result.get_status()
            pass

        # Now post process the data,  uncomment code as you deem fit

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        # summary['num_data'] = len(action_result['data'])

        # Return success, no need to set the message, only the status
        # BaseConnector will create a textual message based off of the summary dictionary
        return action_result.set_status(phantom.APP_SUCCESS)

        # For now return Error with a message, in case of success we don't set the message, but use the summary
        return action_result.set_status(phantom.APP_ERROR, "Action not yet implemented")

    def handle_action(self, param):
        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)

        elif action_id == 'get_system_info':
            ret_val = self._handle_get_system_info(param)

        return ret_val

    def initialize(self):
        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        # get the asset config
        config = self.get_config()
        """
        # Access values in asset config by the name

        # Required values can be accessed directly
        required_config_name = config['required_config_name']

        # Optional values should use the .get() function
        optional_config_name = config.get('optional_config_name')
        """

        #self._base_url = config.get('base_url')
        self._base_url = config['base_url']

        return phantom.APP_SUCCESS

    def finalize(self):
        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


def main():
    import pudb
    import argparse

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if username is not None and password is None:

        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if username and password:
        try:
            login_url = JamfConnector._get_phantom_base_url() + '/login'

            print("Accessing the Login page")
            r = requests.get(login_url, verify=False)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=False, data=data, headers=headers)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = JamfConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json['user_session_token'] = session_id
            connector._set_csrf_info(csrftoken, headers['Referer'])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    exit(0)


if __name__ == '__main__':
    main()
                                                                                                                                                                                                                                                                                                                                phjamf/jamf_connector.py.bak                                                                        000640  000765  000024  00000030461 13645634675 017102  0                                                                                                    ustar 00smasud                          staff                           000000  000000                                                                                                                                                                         #!/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------
# Phantom sample App Connector python file
# -----------------------------------------

# Python 3 Compatibility imports
from __future__ import print_function, unicode_literals

# Phantom App imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult

# Usage of the consts file is recommended
# from jamf_consts import *
import requests
import json
from bs4 import BeautifulSoup


class RetVal(tuple):

    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class JamfConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(JamfConnector, self).__init__()

        self._state = None

        # Variable to hold a base_url in case the app makes REST calls
        # Do note that the app json defines the asset config, so please
        # modify this as you deem fit.
        self._base_url = config['base_url'] 

    def _process_empty_response(self, response, action_result):
        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(
            action_result.set_status(
                phantom.APP_ERROR, "Empty response and no information in the header"
            ), None
        )

    def _process_html_response(self, response, action_result):
        # An html response, treat it like an error
        status_code = response.status_code

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            error_text = soup.text
            split_lines = error_text.split('\n')
            split_lines = [x.strip() for x in split_lines if x.strip()]
            error_text = '\n'.join(split_lines)
        except:
            error_text = "Cannot parse error details"

        message = "Status Code: {0}. Data from server:\n{1}\n".format(status_code, error_text)

        message = message.replace(u'{', '{{').replace(u'}', '}}')
        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_json_response(self, r, action_result):
        # Try a json parse
        try:
            resp_json = r.json()
        except Exception as e:
            return RetVal(
                action_result.set_status(
                    phantom.APP_ERROR, "Unable to parse JSON response. Error: {0}".format(str(e))
                ), None
            )

        # Please specify the status codes here
        if 200 <= r.status_code < 399:
            return RetVal(phantom.APP_SUCCESS, resp_json)

        # You should process the error returned in the json
        message = "Error from server. Status Code: {0} Data from server: {1}".format(
            r.status_code,
            r.text.replace(u'{', '{{').replace(u'}', '}}')
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, r, action_result):
        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, 'add_debug_data'):
            action_result.add_debug_data({'r_status_code': r.status_code})
            action_result.add_debug_data({'r_text': r.text})
            action_result.add_debug_data({'r_headers': r.headers})

        # Process each 'Content-Type' of response separately

        # Process a json response
        if 'json' in r.headers.get('Content-Type', ''):
            return self._process_json_response(r, action_result)

        # Process an HTML response, Do this no matter what the api talks.
        # There is a high chance of a PROXY in between phantom and the rest of
        # world, in case of errors, PROXY's return HTML, this function parses
        # the error and adds it to the action_result.
        if 'html' in r.headers.get('Content-Type', ''):
            return self._process_html_response(r, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not r.text:
            return self._process_empty_response(r, action_result)

        # everything else is actually an error at this point
        message = "Can't process response from server. Status Code: {0} Data from server: {1}".format(
            r.status_code,
            r.text.replace('{', '{{').replace('}', '}}')
        )

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _make_rest_call(self, endpoint, action_result, method="get", **kwargs):
        # **kwargs can be any additional parameters that requests.request accepts

        config = self.get_config()

        resp_json = None

        try:
            request_func = getattr(requests, method)
        except AttributeError:
            return RetVal(
                action_result.set_status(phantom.APP_ERROR, "Invalid method: {0}".format(method)),
                resp_json
            )

        # Create a URL to connect to
        url = self._base_url + endpoint

        try:
            r = request_func(
                url,
                # auth=(username, password),  # basic authentication
                verify=config.get('verify_server_cert', False),
                **kwargs
            )
        except Exception as e:
            return RetVal(
                action_result.set_status(
                    phantom.APP_ERROR, "Error Connecting to server. Details: {0}".format(str(e))
                ), resp_json
            )

        return self._process_response(r, action_result)

    def _handle_test_connectivity(self, param):
        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # NOTE: test connectivity does _NOT_ take any parameters
        # i.e. the param dictionary passed to this handler will be empty.
        # Also typically it does not add any data into an action_result either.
        # The status and progress messages are more important.

        self.save_progress("Connecting to endpoint /JSSResource")
        # make rest call
        ret_val, response = self._make_rest_call(
            '/JSSResource', action_result, params=None, headers=None
        )

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # for now the return is commented out, but after implementation, return from here
            self.save_progress("Test Connectivity Failed.")
            return action_result.get_status()

        # Return success
        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

        # For now return Error with a message, in case of success we don't set the message, but use the summary
        return action_result.set_status(phantom.APP_ERROR, "Action not yet implemented")

    def _handle_get_system_info(self, param):
        # Implement the handler here
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Access action parameters passed in the 'param' dictionary

        # Required values can be accessed directly
        id = param['id']
        username = param['username']

        # Optional values should use the .get() function
        # optional_parameter = param.get('optional_parameter', 'default_value')

        # make rest call
        ret_val, response = self._make_rest_call(
            '/computermanagement/id/{id}/username/{username}',
            action_result,
            params=None,
            headers=None
        )

        if phantom.is_fail(ret_val):
            # the call to the 3rd party device or service failed, action result should contain all the error details
            # for now the return is commented out, but after implementation, return from here
            # return action_result.get_status()
            pass

        # Now post process the data,  uncomment code as you deem fit

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        # summary = action_result.update_summary({})
        # summary['num_data'] = len(action_result['data'])

        # Return success, no need to set the message, only the status
        # BaseConnector will create a textual message based off of the summary dictionary
        # return action_result.set_status(phantom.APP_SUCCESS)

        # For now return Error with a message, in case of success we don't set the message, but use the summary
        return action_result.set_status(phantom.APP_ERROR, "Action not yet implemented")

    def handle_action(self, param):
        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)

        elif action_id == 'get_system_info':
            ret_val = self._handle_get_system_info(param)

        return ret_val

    def initialize(self):
        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        # get the asset config
        config = self.get_config()
        """
        # Access values in asset config by the name

        # Required values can be accessed directly
        required_config_name = config['required_config_name']

        # Optional values should use the .get() function
        optional_config_name = config.get('optional_config_name')
        """

        self._base_url = config.get('base_url')

        return phantom.APP_SUCCESS

    def finalize(self):
        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


def main():
    import pudb
    import argparse

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if username is not None and password is None:

        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if username and password:
        try:
            login_url = JamfConnector._get_phantom_base_url() + '/login'

            print("Accessing the Login page")
            r = requests.get(login_url, verify=False)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = login_url

            print("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=False, data=data, headers=headers)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print("Unable to get session id from the platform. Error: " + str(e))
            exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = JamfConnector()
        connector.print_progress_message = True

        if session_id is not None:
            in_json['user_session_token'] = session_id
            connector._set_csrf_info(csrftoken, headers['Referer'])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print(json.dumps(json.loads(ret_val), indent=4))

    exit(0)


if __name__ == '__main__':
    main()
                                                                                                                                                                                                               phjamf/jamf_consts.py                                                                               000640  000765  000024  00000000035 13645400575 015645  0                                                                                                    ustar 00smasud                          staff                           000000  000000                                                                                                                                                                         # Define your constants here
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   phjamf/jamf_dark.png                                                                                000640  000765  000024  00000112204 13645400575 015413  0                                                                                                    ustar 00smasud                          staff                           000000  000000                                                                                                                                                                         �PNG

   IHDR    +   ��K�  |iCCPICC Profile  (�c``*I,(�aa``��+)
rwR���R`������ �`� ��\\��À|����/��J��yӦ�|�6��rV%:���wJjq2#���R��d� �:�E%@� [��� �>d�d���!� v���V�dK �I���a[����)@��.�����E���Rב��I�9�0;@�œ�r�0x0�0(0�30X2�28��V��:�Te�g�(8C6U�9?���$�HG�3/YOG���� �g�?�Mg;��_��`����܃K����}��)���<~k�m�
��g��B�_�fla�810�������$���������������@ $wi��k  iTXtXML:com.adobe.xmp     <x:xmpmeta xmlns:x="adobe:ns:meta/" x:xmptk="XMP Core 5.4.0">
   <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
      <rdf:Description rdf:about=""
            xmlns:exif="http://ns.adobe.com/exif/1.0/"
            xmlns:tiff="http://ns.adobe.com/tiff/1.0/">
         <exif:PixelYDimension>299</exif:PixelYDimension>
         <exif:PixelXDimension>518</exif:PixelXDimension>
         <tiff:Orientation>1</tiff:Orientation>
      </rdf:Description>
   </rdf:RDF>
</x:xmpmeta>
T�-  @ IDATx�	�]Gu�]=�%k�lْ�<��`�B���!�20d%�KX����V�J�� փ���M��<�q�G<�y�5Y�M���������ޣ����꾷�U�N�sϩS��_U{�ڵ�NӨB��@ ��h�@ �@ pB1p$��@ a1�6�@ %�bP�"��@ �9�@(s�	 �@ �@	�PJX�U �@ 0��`�7�  �@ (!�A	��
�@ �<���& �@ %B1(aW�@ ���G �9��@ �@��@(%,�*�@ ���b0�@ �@ �Š�E\�@ s�P�| �@ ������@ �@`�#���o@ �@ PB �q�@ �yB1��M  �@ J�bP�"��@ �9�@(s�	 �@ �@	�PJX�U �@ 0��`�7�  �@ (!�A	��
�@ �<���& �@ %B1(aW�@ ���G �9��@ �@��@(%,�*�@ ���b0�@ �@ �Š�E\�@ s�P�| �@ ������@ �@`�#���o@ �@ PB �q�@ �yB1��M  �@ J�bP�"��@ �9�@(s�	 �@ �@	�PJX�U �@ 0��`�7�  �@ (!�A	��
�@ �<���& �@ %B1(aW�@ ���G �9��@ �@��@(%,�*�@ ���b0�@ �@ �Š�E\�@ s�P�| �@ ������@ �@`�#���o@ �@ PB �q�@ �yB1��M  �@ J�bP�"��@ �9�@(s�	 �@ �@	�PJX�U �@ 0�hmFg����T�sS�v
b7�a*!����q�@ ���W��S���A
Å۵=#қF]�J2*LAp�g����=���8�@ U@�a�����?�|#����Lp�.��#į@ �@`V�{�k�^����y��gut���ۮ4�
�T��=�bd�����J���U �@ P�F�����)
G�!4M�,�(,�F�Ά�q�C�������!�@ ���+�k d�,ʕ������bPJ��@ ���T�Z�;E��?ך��/�@`N!P�>_M�K�A��8���T��&
�@ P�4�b��uT��IB��Φ�\��4���si����5�ŭ~�^�@ �@����T��C65!GR�@o�ho�u&9GG$h����I��?����HmVz�g�j�����uz��Pa[%_��>Fn��b��V�-Y@	�uS?;.�@ �� P��AyIGM�����4<<�ZZZJ���@���O.,e�߈bL�G�[�Q:0��H�9
G�����c��t��J���#��?��$�,_��gos޳{_Z�2twdS�#��ٔ�˻��=�7"�@ �A��ꠎ!�֦�h�i(���_X9:"!�i�f�{�c{6�±���J1�_�p4���C5ŏ#}��U�%�X	F���`jk�W��S�@ �@��ԅb02��f� ��A�Ĉ�~.D�=}�i@��ֶ����b����^���>��!��(���g����@J��Zt�{��Y�DvP��Jp���@ P]�8��hj>V|�k0��;�8 �`��=i׮]i�޽����idDs����СCʠ)�ԋ�C_�=$?�oȟ]q/���������Y�q���o�*�Ph�ڰlْ�j��t��/O/{�JSO���@�c�����@ ?uc1(� �G��x(azXC�?�=��'�}/�T�*�� ��rP)�25`�v�X����o��Rh�0ՀB�r0����*���3Kȑ����pZ�rI�앯H�\|~Z��A(](�F��@ ��@]Xʕ
�R0$Gá����~<=�a{ڱc�),��5���Ҡ�l�����RYq��Ϳ�����F�9'���KB�<ֈY���Q�ʢ��:gʊ��,;im:��Ŵm��t��]r�JW�����4� �������@ �� P7�A�̱��O�Mr:L��K��ZR��e�)�6+���f����t�,8�p"�
�ߕ�����XV�|r����)]����F�P�F4���YC�E�{��+ON݋���{v��}*�\�*]|���JA	̸
�@ �:5Q�J"�$NG1�k�>B���}��Z���ٞ�􅯥y��ѐ�?�k����7�+�X\���8����ŷs���I5�M���YYG���RSvψfcsj[� ��׫鄁Զ`I:�ӛ�~fS:��i~���F�����@ 5G`x(��n�ǹHkND����R�hd\�o����4��05	�6�(�ࡃ�,�8�����	��`1�ZF�HI�6-R	Q
���~�2!�F��ܚ8�Z�n��Vs�q �F�Hϑ��ڢ)�L܎H���T���v��L��~��O��a�x`��;��F��O�xaT�|ʂi6p:('�	fH�K.��@ �	��SGG�)(��J��V��&�U�L�p�r$�
H���a�Yy ��
XL�g7Z�XZX���U����5���Q�@ �������7��b��zu#z�҈4�a	E�2L�>��~b�%ˈ���4!|���GӒ�Km[�l��c�9�@���Z0V��`���X�g�^�(�G� `��I[[{8A4�&fE�P�B�>�Y	�A�|������/�"� e/�h\�@ 0w�+l�� ?w8D�5������Q$QS#�G���5=�5u�=e�qH�Js��@oz�9�Q�릆2z�o �����,9��C�S��x|߳��0�1�N� 9�Зs�κ�;*�^|;�*�vB�02�2����|pih�/�|JW��Ajc%g���G�s �@� ��ۛv�ܙ6n�h�֭[�/�`[�9r$���?���ԍ��2�I����C6�ǀ�+6~8ڿ��$tut�#}=���'�Z�X�E�_1�NύI�� ��cd�p�|�|)�NSA8�ڴ���}v�d����9s���Çӂ�����^mB�p�"��z�o� �����{��t�}���~��V(�{v� �40�n��ߺQ�����o$d$X� {�i�!ml��2�!YV�ZiO�O�!@���/\�Ј�c^0	�{��Fң���5k�a ((�(��_E�@�}��i������ݻ���������HoZ�l���Gy$}�;�1����,�E� �p_�bP�ʱ(�ϖ<S[X��-�������g��ls&�f:5N-^��9#:��������m���g�yf:G�!|�F�l�QP
�"���_c���@��̛�YQ��%?��ox��oذ!}�k_K��@ڵ{��o�0hp�a�����P�:��b��S��6��I�
��G������4*K4���kO�أ��[p2�g(�,�a2����t�m����6_�4�Kڌ��O6���;���oM�\sMZ�t��$�����PP0�b�P��2*#���ޗ���S����}	�	X�򕯤�z(=��6L�άB��v����A��PjT3���h/,	�"hBks���XՈ����:�F�|��͛ӧ>����3Ϙ��Y��駟��f�3��>����㏧~���� 0'�#m�L((�)�Z�@ �OP�,]b}
��u
���)}�ߴ�M_$?,�|\9�du��C1�ƪ{3[�P���*AA�Z�tQ��^`�ه6J1�j6��3up�7����F(
+W�L'i� �`ɒ%����������G>����*�0���צ�M-�F�"�@ z�4J����(۶mK������Sz����>��1� /�;@>ep������������O��Z������u<Us�f1��z�-+b
���9┄�@xn�s�حZ�ʘ��޽�����Ӌ/�h���0<���G��@��@@)8�{���ϟ���ӷ��m�<��s�'� ��L/���,�9���)~P�!�j׊92��L|QQց���ԉ�+I��"ڵ>s�҅vmͅ�5��Q�mO�n�d+������鸮����sF4�N���'�������0�_0A:�S�S�)��b
��;L�/Ֆ��{��gm�����à|J"�@}#�s���Q>����DxC�:V���~�3b�_#��8^�W� z�f*�IB���F�:�%��nc����QC@f;�p=��u����vj
�)��ٮ����E[lK�K�̗� uAs|C���Ƞ4���&�C(n�(D��aΓ�1��C,�:����Šn���5I�lu@�XgԡU�:�aR�Z���6�.��ieyC6�@���wd�Kx�����G���+����֬�;~tGںe�-Qtg�����=�m�m�m��7c �ړ�08�5�v�_|n��F��rG_ֈBQ��"ş@ �+Z��E��|�,+V��i,�(���O�0�~�/M	�\10%@��h�����u�n�:��
dD�,j.J�C&$�	=4������&a���-u!�Qg;�F&hI�	�\�OB���ל��@�;47��	-*B����$�z%���d&pyѳ��GK���8`�"�PK�����ݥ�P3v s����3��� �{N:e�I����L���M0��R��)Ri�E� /��"5Èg���؞��m�OG�NMY]Q�DX�Ռ� �����n<��G���{�1[���g
#x'}gC���?���o���I���q��?B1����?
l.-R����Q:	����dd漢����������*�ykIо���%x��(Φm�Җ��ӳ[v�1fXq��k�� Mj�dJAN(��d"Ȯ��X{�4�2C��>�5����{_:e�
m�4�.8o}Z*���Cq��"�ߐ�RRf_5`z�r�Йa��K��b�w����e�QD��A��/��k7���~ڦ	�z�) �	܃78Op^�g,
n)t��t�o�Voh��`�j�'Y�ـ�)��5kG�R�	��9��$��V
F���������ՒZ;�S�LY�=�)=�%u�d����ӌ����[�2i����%���uE�س�� ť4�PN��HH�]�a�T��Ӌ;w�xL����+/QY�Ic�W�W:<��<#��������4�T�}��1�	���͡$�f�Fށ����nٲ%�y睶�< kӂ�67�w�xC��O��L%����o���<�t�E�իW���o&�c8F�#��N���)DA(��Q��V�Xe�����$-�hm+����s��AskGj��AGg�|	Rڲ������3���=��`�	���\x�+#�����!5�!i�����;6Hr�G��}hw��NᚲG�\���k^ڽk �z��L���+.є��

y�i���ų�J���9�8Q�q�5�̻0<�	`T��D���@ �-��r�M�.[�,���3 �(6�(�>|J�AN���l��P���Mo|�}[��LA`-�׾�A��~��K��r&�O4�U��Kx���O��Bfݗ�^�+rjkJm�K��i������t���O���>��EKW����tH�l�֠�7�Jkma���jm�%@�N�A��(AH0�Dף�h�@Ȅ+(�]~�YqTʃ6��m-�';��ʌE�������Ұ�t�2(��ieFA/��
�G�~���Yg�����c#��0�3AX)G�������Y�1��8�@}!�N�yv:�WsF)�?3%���Z[Lأ�cMX�zI����G?�Q��E��5�!���j=�8�Ԇ�:���[4c�_R�m�%!���E���j���QS�k!�w��,="G�-[������k
�Q=sV�S����{�P�΂�+�Z@#]��Y�Ulҁ+��^CR6�;����;�)!��:G�;Тc)� ����Q�L�RD�4'O���Cjֆ>��8��W	�䕫�86^��Ϯ}�ֿ^��צ��m?�ʀ+�C�ª��r�����(0�ή���D��E��6�mWP$0��>OȦ]�mx��W�*]w�uE� %d#$�/i�`p�cŠ�"�o0?��k����M¡MS��EU�+!~�����Gߞn��MJ�7hєA[�T��@��r@��v�,��\h�m��"��o�u�� ���������򐅱�7�u�c��$�Q�YPڵ�G����I�C�gP9�4�A���&�w��g��}��'L�lh�h�,LT
���׫nZR��S`&�$�!J�@ �_P�(t�._E��'�}_}�֯_�^��ץ��S�2��1�0o�b�����zA�X�<K����m�9�Hd�^�`2��W��[��&"��%0�����%�@����f��߶.5 ������z�ɝ�����ݏ�h��m�dr�M��z���ѥ��0f~��۴&R^��j!�Q8X~�ʄ� ^�hjʔ�&y9�w�J��P��8\soDG����^`U�'�� �jy��M���<��1�j{�=�y�}nվ� ņ-�q:b�Ю=�P
#:9�|a��׽�:cP��@v�bmK��@9hL��O��6������F�( ��ԁi{�2�ߗ%�O�׼�5v�@�򀵠���Aym����e��Z�t���˗�d�e�mV�(^�If}��m��Ws��i?�������4�I�]/���K����v�[.Jq>̂���gOy@�ɜ�:�����Jiz�^�iu �񘤝�\��b��������جF��"���RtX����E��=����?��靿��Z�y��q"�}��u�����
�X��bA1 �5k֤�������F9O��7J)�N�..m_AF�)�v�{�0�͎mًL���PwL������������ӛ5}��֜��̔�HQ� �}h�J�2�)S=�?��ayK]�)���� KqE:#�а�(���`�^ziz�{ߛ^����r%F	X|�t�8������t��ך	qv����@�zW
�J�o��޵ۦP �{vBt� ��L1�?�����5vݨ�bP�C�}e�h-���3��<Ah�	^FvvQG̔�������]w<��ذ1u/\���;�,Y���4-�8&t�<�6m�ӡ=��K�F���YX��?����d�����?����(��Q_���?1��9bB��+�H/���O<�Dڰa�}aݺui�ڵ��/LW��h��P���@^1�k|�����$0�g� %�����$�0��5����݈V�Pj�n�/P>��	\g#�LIX�XZw�sT)���ݒf�E@��v����t�OҪ����X�v�=��ڥd#r{�KH��	]��S>[L}diM��F��į���]�� �M��KN�L!��O��۷o7ӡ��q8�� |	�8���}�0z�[غ�)��H)��%�{X�����������P���LU(���S	�Sלb���i4�v'$�
a�|^�6�wߓ^�(-X�<�j�E��\�7ڢC�������^1�.W���OY)@�@�0j\���ٔ �$L��j �Z��O<g5�?������	��� ��N�,]�7�XX��g2���:� c@Qȶ��1ё] L
 ��2f\��;E��w``\���5�b �X�A�B#Z�=P�Qp�\���$\w��}\1"�PmC�L��>�ȋiӖm�]K#W�	Ы��z��H�����R���-5PV4W o�|��İ$;Zt�c@�a���T���%ɉ'�*�{vN���R������6�Z�liя�MO��k��[yv��\�@`:`)�g��g��~G�u�b��)��Oh�A=����=�Qw&�!I�W�d�,���3��P�f��Y����%����V'�v���v���*m����Y�1cn]��)�I�ԥ��9[� ���0-�s�)��:����"T�_G�0"���t�ok�GR,Gd3�+l�d�O ��W6��?t�=K�Ǯ����)�EY`�`��'�Ű��r\Gp�ڴς���F(�#��$�{�̂�ŀ~���>U0h�簾�L�0?pP;*�oߔ�:��Z�0���,^�#2e˄���M�,��{|�YO�.{�Z4��8�c�g����r1�����e���j�9w��n�I�Ľ5@�e�oR�B����
 fC��@�oi��&D��=���̱�^�q&�W�^�>��<���<w!t���"�sj�xByr8=�9�|��N�1.���^G�w�����mh�n�:�)�����M��ـ.��ޱq��������ZT�ؠLRM-2�K��<:�����t�զt�#J��y���y-�Ҡ��͛����5τ�4<e�||Ҙ���
���ب?["�]���>�(9��T΢��F�7�]��B���.��3���Q��A\��'�̞{0Ggt~??�jT�/o5�]���1�[��c���Q'� ���n�9�M�j�`��귇���ߛ�3V2���&�c��������L�fqp�/�d�d�ԦMU�F�Ԡ[ԑa|j��M�l@[���,��@X��Vu�)#R� !=��Pzn��4��v�<a��h�0���L!��*���e�~I6o����)#�r�q�$=^������Y&C�z}��!o%�	��C�+8���i����tx�᜿?�4N5�P���qħ��w�,�,8���61��N;ݦ�eE�hζה�`�<�������b�Pŀ�睳�*�8h�W��p�5ֳ�75a�	W����_�˜	(n���ϧF��bC+<�348�Y������V&0uP^o�!�e5��B1�Eʄ�OY��j�O'��$��%�Z���f������՚��K5sX����ֽ�"��g&Cڗ?�Ԣ�F.��KM�a�ә��.<|��=�|"����߫�Ѕ0^�,߅6�q��<���s:yP���ȦR4m�rP}c�tI��Pƅff� ��T؉���VZ�y��5�������ҴB���W��[�8��w�x>�ۿOWmEg�-�i�h�@�k�SL�@`:�H��4V�>q�c�3W���3�_&0��(�����~��\+���X+��>����ϑ�8���H�r� �����:��b �`Ď��F�LZ�'���А�3���>k���u�����W\���Qh�.����]�rشu��;�u���h�c�#�O'��s!8^�4���, 8�����M��7�y������9{a�sB? ��&�c��k������t���W��N�C��O�	�U��X��e=�~�r��e
Š58,ۆg�0g}�[���RN^��@��~k�-�E��"�ԡ/)���^|1�õt��Vy�c�㠃�����`,fQ�"E'00�����Ҭ���G@�9p��I��%\,���pC4��9�OǬ�H�}��/����[m7M6�bNg������e�]�:F�ݮpv!���g�y&�(^�y����s�%6�B�qE ���'�U�V�o괴v��tꩧ���8��t����N�|O�3G�Yy����.������0����� �����7L�3�K��<��������ϳ)(Lho�c�>�5�}�>���OϿ�����h���ޞ��ǩ��C[[�I��O:T��(��qNi�YG�1Q�� �ݻw����V�>���3*�N`���s��}�]�"�ei��}Ԉ?O�f�޽�͙~��'Lǎv���'+Vi���m�Dp��k��O9�t�>�~�z���g�aX�����{>��Ѥ�}��Tާ����5� ���&|��1���GǞغp�6���w��>O�A��vB9X���/�'�|2�}��顇2k���
������׽Ύ�O>�ޠ�k�hO�fo�D����>���/��$tB3m��{�I��v��K���Ra9#�w�
�#��o��7�+_}eZ�n�%�����L����-��t� �tPhH�{���}:=���O+��2�}���Mk��墝�!&pa��.�'��^�^�WL+�j�ܤ�\�UN3WO��Sk̻�[�F�(��3�Om��)����9�tHBS��z.��ff0��iْ�iH�gd�?]���^e:I���c;jXC}�L�h�����tǽO������/�͍��işE��Km�<Џb���_y���g��i�g�;�7J��wQ�H��r��4_����7>�1�?����;�pX
�!cd��ǖ�`|��[�`�0j���J�?��}�G(�/0% ;�#����9������\s&?�3r��s�9�U|mr����y<x�|xa� ��r��w&����׾��t�w�#J�ӈD<�$.����K�'�%�ϥSN;y].����]wݕ�������"f��늑�u��?@lhW|��mo{[�ꪫ�>�x7�s�P"���E�AXS�]�v�����vp�w�����N�>��vU�g����$V
lL�S�tB�G�����WӫE3rP>Ѓr��)`Jp��q���T�QN���?�c�:*�z�N�=���fJ�p�̔���!�|�G�SN�ӫ_�������ɾ*�΢�(����L>��<n=�v��e�����a���2��^y�Ei��>��vƒ{��t�4�44,a�Zy��'Ĭ5��s��ꩈs��+��;�L���g�z� �>�v=S��7&`���>�l���@y��2B��~򓟴�,L�=�qhcf�l�2��3��цa�n*ve�6�3���`���?�N���ԕW^�����t���Z�sRq���w��G�J�#�P=ϣg�Fy�Fc�%��8t�'8A3��7�`q�<_��W������U�Bܣ,���7��F�ܛH0�#r�$�1��ܹ3mڴɬ4�y�{�E]d��$Rǌk��J
�+�����o۔��r��F\,D�y��æ������m�<������~/�u�Y������A�(�%�q���.D��N�ꓴ�\�����>=��H�k��ti/�l,n`�=��܊�uC�@O=��P�5��U����Ax�z<��ʃ3�Q�,X8/>�Wr�5]|��i�i2���==}i�"Le�PZ5���tP
��;S{�R5�nE- R�I��	�8�I ��] �T`6\ڀS:>��ȹ�A
Ӂ!!�`���w_��hB�Q�8#��5��k����u�[h������I,(?�� ��` 0���[����^{m�ٟ�Y�2%�xN���F>��yX�U�n���=�A=r7��!C|���o�+h��>��F������ �H:�%��?C�r��F��J�#s�C��/
�y~��I����6��ݖ)�(�[��A��K��?�������XoLQ��{���O�V�&���Jժ����1:W�����|�rz���������}o���-O�
��=��X��)c>{��C�<�џ��b��D�Ѡ3ߧ�v��z`�l��3uP��.��<@�������iV���3J])�A�TC�I�iz�j��ґCR:5="&����6��`�S[���:�L
���5�@��� ����3Â����'�p�0Q�B�O� ^5y?���6/|���������(��E��Ȇ{.ܜ!sϙ�1D�Q�qςN� �o��D���ϔ
8�#d03pزeK�ԧ>���o�����靿�N�@��t��n-ts\0"L���	�('!_���<�>���={��;(`��g
�r�ipx^��x�9�m��P+�A��?��t�uץ���߰��	ShF8a͂n�Ei����K�Xߺ���̏ �w���h���p��U�xz���ڂp�Z�B�e����������7��,�~�,Yb9�X�ĨPzo������J!�,�������-u�m,P��c���ʯ��B1�TP��+E��g�0hYǐiI+֮;-��5�J�h�Cm\��%�"����R������@��O?�A*���#�Il��J77IqE ��F�&@���w��0"B5�_��_���(F^�-��ٔ�o�R|��5o�����=�sFg��>qv.(�� >������]�"���p ������9���G����MM5\��i4Ip��'�U3@/\���g�`�3衬ԫ���8c���?�ss�$�u�֥m۶&��{��큲�[l,�1�X�m��7u�"E;S��#oy�[�;'�i��E��u˷������]~�~��E����{�aa�ˏsƠ�p�[�0Б��cN�B;���s��>�r���WSx���w&W
�j&��!/p�8�g�BtU
Y�p�z~�	��=�=p�ɴ���PwR����hZ��ջb@ǣ����9h-ͣ�3����ӚU�/ˠ��`[�8�����δs�!� ^3��ÑA-W�� FX�A��W �O�6��"~�j�Gq���B��d��LX
	���/�o#{�)��lLWh��K�"���ڪh��y�uF	�����,��ʕ+m�i���s�~�����1"��O�]z��w��ɂ�X�vsf+0pp����*��xL6�s�� sAJ�:&dOF�X:�6����>f�#�VL�\�>�F�� ���*���fB�<�g�C���*�g)[�w���֔�6��������>���Y��,�Y��hDA`�
4O4� ݼcV$��?�h� ��?Wlh�M������<���&���X�3��dφw���I�AtA;V���A kڿ��|�M��8�5ꈳ����_�w�U#�B��a��[��oz� Ef65*�8�&��L���wj~��Qi�Ń�P�>w<�����~���+ �����S�-�"hI�^�S邳��׫R;�4Up���ԢeNbIb�H��ڽ?�g�V&���b��e����?����ǃ ��Ø����Y���c���c��o�
�`�ozӛlT�"?���0��A�	F��pf�fޗ���@YH����?�1}ڼKW�c6��G{n9�%=i�$�d�z?��ϧ����;mܴѰF0 ��A�v@X�����L݂g�A'Z)�	cY)����[�L�����L�:ӎ��N�+���ku� 8@t��7�o}�[F�G;D�b)���h�ڂﴊ�u��Pg�>�P�FޅF�bZ˄�1�|�aL��C���y��w���t�7o1쬿�f�_)������sӊ����ωҨ����Q^o7�ʗ�+O�w�o�?���5��?J&��)H{����t���]{���"�ՙ�g@��Ay�K}��Y4�nn��~��xg����َs�׊�>��O�<���T�0s�Z�4h�"P�A�~��4nѶ���Z~�y�&�4�J�-}��^�~��ޑN?IK�(�}
!�Y��F5���
Z��E����=�ں���j�V%U|��X߹��,����a`��&�ҧߍ�"��!���0��*HSCZ�%��㞗ӞW��0���&|���抰�V�����>F�(��p�������s'��4(�	ʜ���y�?yS�`�o�D��`<��>��c��䵎�������������0�|�M�<Z)/XP��݃�(���L��/��@;�B#�ڃ*&�=�i��	V���Sǚ�!Oh��9���<8�&�u����x�5�����J��1gEV$@+��(h0�Q)��C��X��8/�nL����@�h��O~�68S������М�������կZ9����ӥ�y,�~�3��?����q�}p�tTJ�g�g����S�L��ȃ{`D��=��n=���� , ��ٞ֜zJ���O����MU�U�*��2TrN�fY~&M���<ֹC��ZR F������|��࠼��vuD;ΗR�o�sb}i����+/N\x~:m���-���Y�LX�bx��P�Ӳ��0��巔��tP�S����ڥy>ќ�����ɟ�%���W\���g؜6K�`�����a�0p�5L�Ä��&�L��X�Q�q!W|OL�G'�_�L@�n:���3�h�S�3M�C�/]��<���<�� ����` ~�t:^������9��)��իM<�����#���@t����9���x���0[L����C=2�������oL��~�a���� �O<ꝴ�.]j��E{kkR���`��އf�88C+��zAhצn.����υ<�%_����%����׾֔+�O~ԃ�_)�>���w�6��r_!���i����Pr	ܣ��O��~ɛ:�<��B1ȃX�����_�0��jE�{�9�Y�u�]�$ሤ&�y�R`׽Jah�԰��q&��R������O��C��:tWf5S)�),K�5�x֙��zKdi�Y�LK�����$��֭��>y.w/\a�S �*B P	�?��_�����F��䇩�v�ȍ>������6�@��=��x
#�w`�!?`�7n4f����@ ��>qx������:󄡾��6����_ ���ϧ�I���i h�g�Ѝ@F!B�AB?��8V�BЂ	����Q�c�=�����}ن<`��$/����A۰9.g^��������fz�zx��2P��n}��@��������&.t�g�D|�a�/��OI�t���$-�P6� P���&6���׿�.��SR,b�O/�VY��O���X�|�-�N��Ǹ0_�1��-��<��tQ����[��H@��PY�ֈb*����o0h��D����kӃ�>��x�au��i^gw������Of���md-Y>�y��X��h���,�[~��5KM��E�A�ǠF^�ڹ��ZZ�4��o��W\xn:��5��3O��� �h�]�0�!��8
�L���q��g�62M���n�ݸ�@�<�ꫯN���7�֭[mi&���Μ�c �&[3�d�v�CxS�����r!�'�ـ����Ǧ;4<s����a�~���0H"0QL�+W����_��l)Lք�4e%=�	�3�G��8��B��S�\0P>$�Aq������\#Hq�c�r����}
���Ȟ*Y��J�*@��'�{�B`�EL��/u�pq��n�%���\>�<�f�������ukM����txF[!���<�Lk#�^ri:�����5�혉��#��&`�?p��Z(�y�\�[Q�����B9a���H�`��P� ���JU��S�j�`ki����o�r�ǆ�M���P߯�뭞)3����
y�(�� �C]( Ccq�o����Δ�����*S�s/<�]��,K���ic�V-�q�>�y��6��tA_~n�I��0*v �j���8 ��ޜ-�NK��H'˂�Ng�u^��+u�]�;��ڴ�tquP=(L"�"T*�����ݺ-ui5���U�����䔊,z��B fN���H1�3� ��cQ�j���W^�JmM��������'���I3�G9��&��v=���y��.H���͔η ��G�aZw��$褿���e~fɴ�.p��,c�������o�ٜ���p��B�V�� �Ic�,�((.<CX"���]1����ӛ���t饗�I)����k�ݜ��  @ IDAT�6�쉀�����L�u��V�|�S	z�Ju��ѝz�v\iP_����9(({.`Qy�eQVQ&j��Q5����˿��E��I��&�eeKc��k�%i���馛nJ��v��	Nކh[Lm���ZY4��"K������h˼���4x ��퍺#�1MA��y�0�b��TSä�U��k��*�����.���Y��H?�
���[AW�6�Սb P����U���<{mgZ��*9���=j����d�V�U,�R�F�tA��k4�QiKWH1i���-�֥ ��>]�0�7�����jG��� Z�ߔ�b�2*Ԧ�I*�M��gN@���}�/PG�y�bP�Y��N�� !����H���fȷP���B��A�}�������V�k֩sF��YG����?������<C`0��9�>!�(����za�Ŀ��7����M��&�Z���Y�%8v�)��G���Hܰ�\|���~뷊��zl�O`A'M�ǁ��`�.� ����������L�һ���(YX�At�w�R����L٨w,5f��Ee���z��C#���'?�3���Ĺp�y� ���my$4�ig<����R�����];M9";:2�w�؊���Bev�m+�!]�g����-٨z����P�=�Eor��P����xU���Q4�[�8 �*R�N<@_N�Z�d~GZ��Ti�Z�'i<���B� �[y�Pzv�)�������c�:�9��hK�|*Q�j~2�2ǚ�\��e���A))��7<��#��mkKCc4D�Ԅs��28gx<�ٿ���j#vF����L�-�BˊBA#�y;|d��\.�Q�ͪ�g-j�����f{��פ+�����o<bs�6�Ո���;p0o��4�J
�� -���f\�@^�Ӈn�,PX��N�|�ܔ��	؟���+
~���ʑ�NZ����p��F��:� ���_@�Bt��m�6��}�'J����yNoʔ3�	����mkeh�9�\�s�6Cz�I>mڥͿ.�=��9JΣ̣�P�T�C'Vp�v�{����8�����-�ȇw8sLH��+��֮�ޟ��iAY���F�l�6��(���h6V]x�&ʧ���B1�88T :��Z京5Ҿ�'�ZlQ=���ن[���N�����ϥ��X����9"��=�Y1DI��}�@MB���\��L�[�]�xf�&MW�c'Z7o���R'��#�j�0:F��/�����Y��R��rs"���(��{_t ��09!��>��`mV�t}��2a��/���'���"L��`���B�G��ʀ ������0��zȏ����ƙ������c� �w~�yx͚5�w~�wl�e�F�#�	ܣ\��҃�z@)���$�+(JLװ��׿�u��)��IVD`��߃��5X2��e�G��o��ٿ��w��.�������7S��+¬�QZ.�,q��������{l�D%��qq�X<hoЋYGD�E�]�t��mS	���,���5��e�T���E�hoi7��_�.y���6K� �z��~�3"@�N�!�Q̗�M��u;�~=ޙ8�o�8 ��A����&�T&�CV*��k���lu�(�ou�Qi-�OP8F1+)����i��	f-�³y�| ts��ݩC���*>��Ft"ɠ��
C'j� sgdh�[��vJ=A�+�^�(�T���1����}.�w�8Ja]�s�7ה�~�y2�߁�1�/O�<F���X}�j�a�¿C�o���{�>��Q�1K��	�kLIt�_pነ"�'��<ϩ�F�z�>�M����J���������@?ńL@x��4��n����n��g~x=���녺��G>lS���I��`�g@� l�|ݐy{� xQ�ͣȼ���oJ��@�����kh��<���e������m�,�G�}��S�-Fy����_��Ք{l~�Ղg�'*}+�!�i&*�E��i��@<�:0koA�{�>�o�8f"Ok&ϓ�3�c��E�$tzΥCK��;�6!��]�}W�&[�[�h��K�Zm�,���Ќ�a�pF�g'�P�� �,L��k�V�^ Ԙ�( ��|�I�V.��c��&z���y��<�������'�����=�u�9���Q�p��+��gj�K<,(lȅ��e���������L�UW]eS+��C�D+e&�|���E��l�N�3��6�P���q��}�#4�G�(��6+��|;��ɧ7j��O�b��à)�۵�\Jq9���	�jɪ��a�b9����L��ˊ#F7%W*����sͨw��	�g�ʞ�6�>��a&�	� Ŋѿ�y�y�ٲ8F��L��<}t튁;�1wo�t�䩓׼�5�o|���ʌ�П�m�;���_���])�>��xξ��y�EI?0�G�3�êAg�����*�	��Pa��b��a���^ݳo8�ܹ�H���C�C�2F�0��?��9 ��
 R��"�u���C�o�#lF��'�'�>��~h�3H�:��Ҟ��BQ�d��w��H��p�sSz��q\8-� `���$ͭr�Zi����̏�����*�&?g�q�-��$�ݙ^p
�1�{3ȏ��(��	�c2�����	����8�������kz��w�{�{�F��-��$��b��!��2��6o6e�(�g�ߟ�[�U��'Ø�I��3��{��z�8�St�;��]xᅶ|�Q�d����7|P��3�?Hה�)T4t��~ݺuf��>�����NL	xy�`Z�/k�?q�����0�Łw��Ƿ_�����2A��Ϡpx<����3P��j�$W�<��>�j�.By���)�L�Q��5�u�\�sa���(�C��caB3�*����)G0(��Z˜�����5�@�g�R��}t�ai�l�a��9�5�pȽ�`4�(&�(�p�+/��p��L���1#�<��L㟯�ɦM<���@w����4�}P6ȋ9z� ������G�E������#lhᚑ;�� s��xp�����L�SN�����C�<$�I�������וޏgSG�!d#bw6�&�K�(C��6݀"�/���t�~kq���u�r�ianM��=[8�ӗ�i���1����C�tVvx�G�}`@ԅ3"���٧�~)�3<��8���d�7�>����s�`?���,���e�(Fۘ�	����L_�OZ>EpPK#�@iᢅ�4���K-^Ǚ38"�׭[g�"��㚑<��y��nL�u.()����Ho�t��"� ��j4S�V�z�>
�s\U_���-�<%�-h���
,U���ߜ?�9J'�g�1�f�\0�@a2����?���Q�|�'�v9*F�G�6��0�\A��%�BF��3��>��&
2#�����^BH�C�����>���ng�� E��z�޸&���#X�ϒOtx<W��B��}1��7��S7�Q�<-�8�?��4	(4�6W�*%-y_��bP	��=+��1�t��6��0�b���AG���瀿�y-`0T�X�h�=շ�����ٷ��.�o�GHd5hn�n	�`��EN-���z���=�9�eEx51r��7;���"Pl'��f�)��S=�Q/��F��Q�h&�1�r�Jx�(&���!�������3��{Ҷ���d���0b1�`���7���'-O��9�6%bW��7���q튭��*fn�6��I,��f���7!V�{Tzw��Hׄ��"�H�2Sv��7��zX���ȯ��5F��O'�_�c0YZ���η%h�@�������d
AJp|ȟ��������W�{yS>
���1S���X�d���rYY���J�@7�"�E���naZ�һ3��R�y��Fl�:���-�3�i/���L�P�4���yO)?��>W&�h!�[~OLY(�;2}z�PG��
(�h�A"%K�|D]���j��	��H��^�����t�B9�Dh� ���3�j��6�S'?y��2���v9G8֯�=-��۶mKO=����`�3;0�{~vAI^0u��֮]�.���t͵פs�>ǖ�bB�@|<(Xصo"��2��?^�v���l�>���e��|�;��,{��_���8���'�lE���k�L
�ɖ<8��d:��&J �;�oA�݉ޛ��c�E�ȡa�F��i��j���G��G{R#�c"�41��^�I��� �߫*n�&?��|��]V�#0G�7x���Y+a�jg�2�)�w�#L�q���<�Q�9_J�0�$�/=����B:cݺ�zy�_�Z)�32#�o����|=�����x��ibW 3�����)�˖f���N�7z��f�ŗ��ȗ��4�W�����D���d��)$���⿫u&?��G���AMj^H�RĶ.폭<�yf���!����Lѯ	E���! �+��@p��(�3��1���:�1��c����xu�a�os��a��}�����?�l���Ι:�0z�����t�7�7ﯽ��tū�H=R�����?,�E81�̖����q�z匢4O#�|�r\ˀ�Z�Z��f���0zV�b��ϰk"P-,L��M��7@�d�pO�C{� o�R�`��Ü�:S+Zj�O(UG:��Y�0��1��j��{�^���1������n�|�B�y��fc�b|.<g"���p�<�Q<������3�' 0�A�6�����X,.�̖kg�\;S&mW<��+]F��!-L�|���~���{�������uS�bp��R���BS�!��M	�<s�g�	`��C)������j���#�<y�U��QQ��:�E�nũ=c�ɒ�<6(��7����.�_)yE�V�r�mҴ/

gB���2��?�� ��a1�Z�eH�ƍ/j�T��Ktn1��"=�rP���@��B`�Y0'�̯��3�F3jdZ��[o��lذ�<ϙˇF�/����r��#\8�n�">��|8@�a�s���?�7ǃ>�~���m���w�����wPd&�VM�&L�085��2x�\��}�������L?~W+@yq�ڤ�Dx��oJ��1��i���]�t/��#t����qǺ�}�.�Z��3�s{̸t3�TVS���p���VRz��ǵ\�%y��tPf�/Bc!`#	�G�w��V�ܔ��c��}����ŗ�%�ό�p�d���o�g𚏦��`�^~��93����`��EY1���j|�_H�?��m�v�Z�d�cP��ͅ�#����E�lO��FJ��hk0�@>���u84"�F��3�PyN����_ ��'ǉLhn1������VR�1@�����w��^��*��x�Š��#'�<�P���������j����"Kr��(��R'(W�Lv$?M\p�y��U|s���ߞn�����c�e��+&�ԁ9�F��CXÌ]��p��s�>¼�0C���5qP�Y�۞�5ۻ:�F�.&k�A����o�U��G�� ���T,d<�̔��$���q��ç],R�� \ɟ��M��A	�4q��3�:�ՔB��QL�	��M�T	��&�u<��'B��D:�3;e��F�y���>�$�̷�<�!��HK�1΃��܎RxQ����ٰ�!1�9m�
�14��Q$�_��+��1"�,��QOA\gx0e��g"`r'�6�!����~:}�ӟNw�qGqD}0}V����3f�3��>��FtL1��)/�(\3Z%�(;� �O�~�����srP����]{��D�i'?��'iN�p�s�n9��q��M�)7��	�8w����d�V����Ɗ�F�����"�J`
���nQ�|����s*;�/{�OFg�����	�=a�W߳�z�E�@^�I��s!�������U��N+׍�b0�E��C��1�řB��������Ĵ}Gڰa��y�:�p���R�����Ab���TQC'�s�0u��P��Ɗ�{�'}����%�h(�a���0g��>�E�r����܈s@[���G�ܣ�#X�ǵ3F� >�49ȗ{\���vG�k\fr�F��F�%����B?#
;�A1�'.���}"�Fj;����x�L�5puH�i>0��CH�ύ[���?+G�v)
���L���ɣ8С���b���9� ��}y[c����E�>@�2*D)@�0�� �s_o_�K��a���%����<+����̊�Q&����R6YG�G@�3Lޔ���F�@,]�4�?������<�P0�3FY��b��b�4ȋ��ڏ�C��L�ɵ�S��(�Q��f&�F�x2���C�ҖV�ס�`����$1!�޻Y��E���/�ʷ�99���.c�,Md�C������F-'�6]^��=9hO]�q�'?�I۽�Q9m� � �� �Y�u��<�����O7���O<nK��{�ڳu�֥SV�b։SO=�8�G) ��#�ڰH�6Mb���w��`V)��
��Wa��D:�NƜ��L���"mh�r��F���|��R�`�'�}��4�}��J��N����d��@��p	�T��a⌦؊�����>�o���V�K���p��Ͷ���i�M��4�����8G(~M��oī�/H�����]w�e)12G��G;m���aԎ�g.�i�Dp��(k֬I]tQ����s�k׮�4'�ǘ��W���7��;=�P��7�aK���o�
.P
P����d�?O��}&P��}���S�wܒ���y��):�&*��a��ͥ���y��e��'e�]7z�B1��&�#�Mqf�D�����O����-~�p�v�[!e��L��<�q_��4L��j� �����z �h����іl%�����t[3}@�� �_{���}�{_:��m���A��e*!Np�>&H%L�G�?���&��/����t�M�RbϞ=E�hr���z�$�^�����=����A~8�l63I���S	�p���f<��H0OVTVj�i>�$��p�uG�	
�`��U�� FI�{|�/����-�KA�<��l`�-rNq&�K?�'7�ʽ�'�c@�:�n��m����S�=�X�	�R@[�=�0��" ��S��+�>���2}��� �Bi� `����q�:��&���oOoy�[ҧ>�����ͤ��>��|���7g�������tΤŁ������I����L�QzI�q�V���.u�G#��x8�z�x1��>��8�|t2�3�2U�GFI���#',b��HS�]���-;�m?�qں��4��?ߵ0ּl[GWj�^��2��k"6A��i�Z�YXݫ���������/}ɶ!v+ �u�`F�����R�>����}�{ӟ�韚R�K�`d(�v N>���ˌa�g�O�t���p`�`i�;��~�zK�Q���k�~�SpkH=�4-�9���W�!Os��8e�����6j9@1@��7(��Iu֪k1�>1%L�y�����l}%o*�&� �؆�j�6��,�;����>-g��Z�E�W�ľ�;KOlڙ��L������ѭ�^�̆����4��2�B��ʢ����Q�b;2��70�m�Ñ��)�xWQ�4BɌ��p!\���_#��^;e5g>��=��0�?�8 �{ ���\��h]�[��S��"�|�ɫN6+����~{�"��r���h$^~������Owl�S�6~���gLa�=�Gy�L�|�v������ӟL:�������<<_�]>�8���e��St�>���F{��~�o/�=��h/�IδO�?���׹��SH3���x4�N��J�s]v-�N?�}$T����xi���PT���o�7�sX�X�2�����*�R��G oS����G�d��p̳*7H�.HӐeS�d�qg��v���[�J�����pZ��L�Ug�~ȣ�=;
)�� �3����Ut�����w�ީ��*��)O'�ƺ��3�k�ajj۶m�l�Ì`<(#f��=0�@<~��MoL?��!{p�f��f��аr�JSB���ʦ5PXPb|ʢJYW=ٙ��j�4V������{���f}lhP�@Klѷ���1?�]�p�r룆
��l�7^"(�iN&Q�q��BA I���ص{$m�r��[��^�����a��,d�D�pb# �~�ԨK;n޼٬.�T|�E>�Fػ� Ϡ����;���R(*"kA�ԁ�>�g5�@y�%�����m�S##1��z6yW���[�7L�щ\k/�N��c���m:�=�6M'r�u� ������@{p�E������4S��G�����.H~6�E�g��X��'�%]`�)!�,�9� Ҡn���i˳;Ҷ��i��_����p�IƬ>�Z���{�*JU�ud挔����{��L��Ā�H��#�<b>�?�M�d
/�y3�k��+���{�����FF�^�%�G�|$X*I����׿�u3%�'��z�a�)�W��f��U�!O#ѝ���<͍|]�����!����=�JH�5@��ڏ���ng�ң�ٺ���ܷ���yYzI�W�Ŕ����Rza�.}n���/�Ч�����R��8dJ�7��wI���&(�Yyw!��P.c�*e���� �+�� F�YL�(ϛ�d�ca�b�nݺt�UWY{D�=:����t��}VE��2}��믿>������@Lf����a&�(�W����L�[�4�]ʻ����¹X�Zqy�i=����@��ʴp��_���g�i����g}6��g\5��C[[k�v�����0�㇉:�Ѐ� bf���U��ڔ� �-A�r-�)�ِ�a�<p!��<�����'Ɛf���Q0V��{��ڟN��)�y�f[i`�_S[0x�1��"U���/�ܲƑ���qL���(���Cc�w=��˖����4DP=:�yz�������5|�ͦ"��?5Pp���pB�'�iԽb@�=؛�}?ٔ}��t@&I���-�ȉ֎
�s�ő�:�ܓ���x�Y¿U_�l���k*f�1�Ac�M�6X�mg�U,��Pz�2�b��ג�.�!C��mǉ���L�j+���}��i6%ڷ�%��a����R�%�k��7� W^y��C�=���ߵPZ�Õ��=�۔���>��6��P��-�;��C�+�M���(Zk��E��Qm:Kܢ�9M#�{�*=��i���Z�@f�Ś��M��CG�ʜZ>��c@.��{��.��f)�|3YIҍ�R1׶Hoׁo�	�b�����,8I���6}=q����6�7�1���O�x��m�Y��� �x�#p	E�@m�b�@>�sL���`!�����ն@��@^(���bm6l J��3U�@|B#P7��k�Ra�o��q�g������LCM�i���o==�{�L��H��Y�sᧄ��l��5%�K~	�5*�Y1��`*(�v*\��u�?A�����VO4K! ��25�b^'�C����@X!��K��u�Q5�z�3��:���P�B��@ܟ�Ѱ�.�{�[Sh�d(߂!)�]hA����|}����;��}h�5��v����X�
@	�'­(�����*� l�R#!��d�gz����y)]��P�����xg��ul�Y��u�9���֗��gf�c�s�8(�զ��8Μ�;�N�rU
ַ�j7�Lz�	~���t����A{%O�7Bb��'trx��=!�h;�rovI�����=�l���=Um�h-N�Kw�V<�〉���0��d/Y�H�t8u0�ɬD����K	#I���B�
��? ��c#b�,��aY��?0'��Ǚɑ������V��+�����}�]��#�@����1�\v���&�^=ũ���H׬��q�zn�q31[�hP���/*�ص�劃Ǜ�ٖ3J9��b����^�X����@`�b��H`N�V�St]�[(y�Ug�3�._3�Up<g:�H/��5-�Ƴ|�_ղo�����I����d�,�i)��[�=�RPx��'s�)((�8����)�S<v��TF�M�yk�Y��G�ԍ��ϸ���}�lNk�������`6
>C�!�glԏ��L	(�M�C�L��Bne;
ffN���!�j�<�`Ƅ�<~v��n�}�b<L�Y<���Yü���ЙI����h����O�Cr�����p_��Ϙ�'l+q�j�+L/`��v@	Aq|����!�gp8ϷSd�=�ˢR����/�B1�G�>��e���i:n� ߄x�PGvo��&�]�{�I���QP
�6`�����3��w74]���
�}%o-pE�w�}�YP8�"�X"jP���λv�*�>Ԋ��'�*�w�S<=ڵ��)����u�8��D���+`�V)�[3��C��}̑��u��2kA&�]�O��*E!Pz�G3J��_�'S>�J���F�����o���`l��MaP.��p���﷕n�'ƅ����9���緾�-�F�2T+�H7�L&U�l�dg
���׀a��@E���an�:0�&S��,�#���|�Ӏ�,A̮�k<{^~7~�A���N?�����>��3>��W`P��c�߳w����NO>�7�g�k���R�я~d����t��^ 0S�b>fz��
��ǌ�@7k������f��+���m	^6��o�d��"�q��t���|2/ V7`;�ʹI�6k/��,�H��@i�8��9u��"`»�C#t$�N�FAy�a䅫�U���i���F�l
��׽.��8BAos����o�v����3J��?��w�^#�n����w��J�ܺ����S6���Kǅk����:��;CR֭����֜"i�LS�S��5��&J8��������g�|�"���|�\r5����>2�w�Oxy�F�:�L;�~cյ�7Sg�/��WƔ��1�TQ(#4{ZnM3�ߤ�����B��GV�͔��|�g���^#��[לR���߳���҅mvr˕��-7>L���GȟC�\MD��A���� <�{z�I�	V��o�9�1�$!$؅E ��}҃����B\Θ�B�	g��"�p�y�eE�I���oOw�q���-ſQ�C��~����b�0��i���#Hg��YR�/C~$�M���200F���\ ��yfG�S�Fn3�t	��櫄�^��'X�p�7�O|�}Ŋ����B��	L�����/_^�2�?�H� ������<M�`�c�Cɸ馛�W��մys�1�y�K[:O����1�ջ,��zR#��"��/���v)��[�W������]�/����BdW,&�nę:u#u��<1`D�z@�L�bf\H�ۙ�?������t�nݺt�%��7�Nv�ܙx��;�L������e�b=��5;�X8s� 䙳�;84h姯����wQ
�򕯘r����{'��;�� �F&�����bU��	U�2�t�m^����6��w"=�k�vv"�ei,�r����X����;�$F��V�wBx2�r�>w�tilڸ)��o�f��_�4���wz���c�@�sF�p,,B�V�f�������������K�?�|Z�tiZ�x�Y?�9bi�Ӫ�k�s�g3��<��|�]~�ָ;��Z��՟��"�K����@<�*u�%r���Λ����:�5f�B����Ycv��
q��thE�c�G�"��9��t�5פ[o��SG{�0�|����_42N=�����}6��͛Ӈ>��t�E�O iS�ULW:��9g���O�Q p�bځ���{�M���w҃>����c�'�*�4eD���_~����?��h���n� ̩�����{�:;v��p\+ҀuFm����)
k��E�K�o3[�H-��c`�L�j� �J�%�cƛ�M3�r�7^�r����^�6mڔ6n�8aJn�d�� G@s��u���g�gv��3�H�]vY���KӚ�֘�F��z���% �P:}��t�}��Gy$��7Np�$4C
 �������',l�"P�|������@���35ŕ�d���c}�|��,!�c4�O�#;���r������yԍb@cU;9&x8�A�� gZ��Ly�瓹�z,�y���3ק_��_J�����޹��Udy8\/�1�l364�!�=nYͣ�-5 ��%d	X�`A�{�,{`��,`у�Ă	+4j�A0� �X�1P��U��s��y�neefUf���(~Qʊ�{�F��ŽqN���?�ϓ��ܱc�q�3����qW�B��g�yϒ!�����]��(���'&ӕ�W�=&�N
��~���	���َ���(�Ј�S�S��:��O�r�球��Y�@ojk`zECf�_o�g�a�
mEW�v�w&�T�%���}7mˈ�d�|ű
�K`��-�?~�v�ug����g�C����ŏ�ƾA���)���{�ϞP໻d�-�7��
<���FAv���]�d��?6:���u��<&�Q.�Ey��9�u��&൫�\9o��!�������5���s������ɇ��'�]��1j|�@H�vO����W.'lbb$C���
c�|�8`|0��'�U^���#�v�3���C�|�N`� ��\0��;2��ۉ�^��k�s��QW!20ve�ʲ��R��=��l&]$��򸩫�:���}����u��\3\�qϒ�2vqz�+�D��l��]�f$T�e����H��H��]YT�Ƈʢh�z}�7$��M	LL��ƈ�↡Q ��)ئ�iG� F�Ɖ�ʞ={|����>����_{�����2��	���S�����8u�;Ú'�&�ý�dx������sh8c¢��?p�<�4<W�p|{�����w�F�20�r���a�Xaw��\h �q0c�J)6n�M�6�@1aef�=ا�W�WLC�5���_z�������Aas��k߰q�{�p���ú[� 90
�'i)/�$�FȽo�>7TH�����ĉ�O/���8�"0����`��	�8���!��^�=��R��c���"c�(��3���peA��a��i�F͕�0�0�6�7���u����v$�4gVwՁ0�'1 ҡ|i|�p��ÙI��J������ @	����5�Gqs�yq�u0B0�g<�K���׮]��ٳ��¶[���Ǐ�z
�U�A'����!pc��1�p0�`���L��!?(�a��X��'�}��:�7��GR�lʅ��ʊ
#�����&''�@�L@CR�Dl�aк�hlP�4P4B|P��(q4�����i�޽��W_���%͸9����5r�?�>��\䇢�*��x:hHybY(�//�%=���>q�r1OBA�@x��AN�k�?��~��t������y����P�	4P ����;w��
�8`�!��a���lQ11�ŉ�Ҋyw��mc�;���X��#�8 m�0�D����P����;�^{��t��)o������c�1��K�8�:�C��A��#����@+�2���裏��_~ٍ��(�=
�U�A&����:�smǶ�ζ��<9���DC��ed��{��Č��v�-���������qŇ���5W4O&(�A��;�LG~��;+�����8��I�2g E�1��P����s7聳���;���_K�._r〉��a�A�d^���;=�1�$2/^��#0��=>����̙3��1x�#�^���S	��E�@�{�'c���~�7T�w������%��%��𛴹�>��`Q{+<���u�l�Y�T�ͦC~��#ij����Ki~��MG�Q��9���fΆ����3,�Q>�h�-k+�<>����f|H��=��U�=wݖ�+m������Y�.���m�/=�H�a��Лz.(zܗ(���{/�ܹs�>H}������C:2�P��<��X	�/�ɓ'�s�=�6��SO�>�a��o�"0h��x�m�R>܇���x�xl�m��F:�B�a�����n�a�$0���g���������ϙV��@l2��5l?_O�6l1Eo��j䥱<�v3&�L�ih����٦���x˹���H�#�y��ofjzE�G��8���[���tê"'rE~��2�"ifM�b`?�P�f�t�3C��C6k~o:x�^SZ�Ga��1ɳ�z�2��-�C�>�������7=ׄ��@���Y����`g��+���=����rad�;g��?�8}���E@nB�F9W�qn���1D�6���/�/`d�>����������'^���׃�{��o�"K�Gy�5����ٛ����O��I��|c[�1�X@ꫯ���C�F !���|/zC:-���X���&Y�
y����PW(*�w�o`��
���/�E���B�"c\��N ���F��G9�G��_a�	��0X�ɠp0x����O[�(a�z������x]s�-&>6<ܼ��	
ŵ4�+���k[�y|w%j)�=ڢH&�ݼ�g���/4�B����W�)�f��[���v�VRs�_�x9m�m�+L��`	���Ѱ�j��s(�5YO��o�I�ϟ�������}@�͹r�a�!ލ������z������?=z4�ڽ��<��c��[˂�!���˝v�<"B�;|c�ȀB	%�j��+ڄ<�cq=����w+ʼ��8ڢps�⮟�V��^��K�<�z��aȰ����jCB�bHƶ�^#~��uL � �`�k��X�e7A�����ݮ�����C�����k�~�c��
���*���g�E�:͵0l����h�V����O<Q��"��t�A4 -6��F��c��#�;��C,]O��D���d�xi��Ӈlc|�#�R��gX�����m�������w�q�[46B1��O�#�S��L���آ���7���ű��D�����/��_�}�t���{��t��'���b��ut���5�+z����6�e��>�5ĥʱ^���r����-CQQ7J8;��4xht�#�B��5>s��A<fs>���.>�܂E%R�T*��(��SʥR�;��@*5	�|P�H�R��>�i�Q��ɛ<�鱲�B��7&� `�A!�dDQ���eyG�GLLp�,�@x��S�q�J��D��9�F+ɧi0�Xf>�͹�F�q�S/��M`�_-���y��,�/�Y��⏼�����8m���\R94�|{N�ōlh`Ĵ�)��i&�X+���&.�96��M8q��
î0��QsKcs�6��m��5�@>s�C+�4�8�Y�����&rG�<6X1,*&t�7|�/��3���'*�9�����:4`9�%!"�%WUHe�\;��"?��b��q�B�L��i1H�b!\��Fōw���F �]�����+d(�1����UȌ��1��4�|GB��HF~\��uK�w*���q��h"�j��Ay�B �ޢ���kpH�Mql�����7P83��,ޭl��	(�!Ma� ��i۹���Ƀ�co���G�o3Q�O����M�6�#���3���"���5��|o��\�|�V��$����fQ�0��,����&�?��h��mJ�~3�q�h`��������b�������U�9�2Fo���*ۋc��PH�8y4k�z��1�e��@�S���#�\�R���"�ډ�}���C
\��e����e�a>�_��i��S�l✊x���  �IDAT�J���2s>��[9Vr|�1�4��b�ȻY�دxud`T�Aׯ��q���s�����ef��ٍb�7�;����m��JwiL1�V+�5��xKg!�kG~�X�QsŖZ�S�X��N>���yѣ�i0o.�y3b&&��H��ϲ�{��d&�T��k���2�P�d��(Zb< 0�wy(k΋
�q��(6�(h>�k��cH"D��@O<�l'/�)����6� W��HK�(�;�ws��s��/� ?�pc9�1�kt��Y�=p��Q_�W1�"e�mG�Z[�
�%�p���ܶJ�e+.Jk��U��aO#�ʍu��|g�Y�nض�1 �}��]U�hI\'�ǅ�R/֨,
42���%X���X�
�q����m�����'�ߜ߱���+76P LxBIhdk.\k��#�&��W���8�b��sA�G��%�5yһv���F=���P90^��⚈c��\��F��ZFA�y#�h_ܰᚶs����s�}����L�+�+fq��!��T�쾢���A�2B��\����\������20�t����UR�7��8bc�����y	�
x�	-����n��c�YlZ7)�v\���3i����^�� ��h�{ix���X-J�ʍ�����r�9u�^^�(�╗TN�v�'���^�FuH���c9D�+=����N�(c�q��f[�Ȕ���W1M/���o(V�f�{�h��%k�}�M9qn�G��خ�;ݝ�ݭb_�E��%K��$�F	#�����ʂ�񉞵'�?Ȁ@�]��a�\ۍWK�v�]�9�n>�ž��`07"��a�@�X�Sc f��3�H�XD@�@^�A�w����-w-����]�1c�EwhxP��E�>��q@OB��Jt�&��P����v�܎c;؏�4��܏�v�!�&ya� F��6�b�� `$��8�W�N@D`�	daب��xg^�T��q�W�&�kgrd|�M����c�0�#����>t�� � �K`&'��q����2�
" "���[������K+�#W���T�_P�햿�w~�T�w�~p�MNL�K��S��}<1L��u�k �xp�y	���l$���4'�U��v���yh7^0):+w-��{{Vݯ�v��_N{X���dC�_�!�`��=��3�����tΒUD��I��`�xUB)�'�,�����;-w�W��2Y� \���nq���"6�7���x�����J��+z<xP�����[
y�=��`9`��{��H��" "0x20�V]yоU�o{���~�w�r1�ؾ����_��� �)�X	.��X*�!�� ����ߦ�����Fxȃ��c!#�`�Jb<�/����>�����	db�b:B� �>��]�۰1�ҥK>��?�	�H�g��O>I?��������t�C�����n@D9~����������.���n�d��o�^ ��F���F��=x�������o�잁00ȃ�y�=���Dx>\[Ϡ�u�������^�VY}#��F�3l��A����5�Xϟw����w����NgϞM�op#�y1�#�|1� <�����(�)���@N4��SmI֎\��'{B`�_xn}�7�CaϞ=�/ʞ�2g���o���z�-��sܖ�[� `N166`r"��\���m����y�tq�b��;<O��\�0ȥ�$g�����Ǣ��0�����3��� ����ӻ����K�}�%oQ�+��tL\��?��k��7oڜ:��;��/�w,��~�a�/�*�g���駮�Q�,:D�br�=<u��?�� � xf�fk/EBؘ?�a�����l�����5\�q==��C~n<� " ��a�[�I޶	���/�{����8���b�s�siz�2�0<d+fZ2��M�6��^���@�Y�0=3�8���y��ڵk�ih[` " }$�ɇ}���{K�8鰝�1,x� ��9	��z�xf�=
<���/�=b;^ȉ�<9Ֆd� A��=+�/� ��1��<�v����p�ԩt��Oǣ�<��D@D ��RS��ca�q�nF,s���Oq�/dts��)�>}:=�쳉��A/Qr�'"�y2�,��9�n��(z^��\�l`#�p�ĉ��/����L<d�"�)���@Nd�T[��ca�A�s`�%��o�1� �1�0:6��B`�/Iz�Gҙ3gj�ɛ4���T�!Z��}" "0(dJMH�R	�1q;���k@�'����O���z�1�p�B����kk"���'�~�Ȧv�SZ�+}ů�{I�� ��hȂHS6����K��퉬���j�#�F�'�Ĳ����D@�AN�%Y;&�Q�� =^�<~}�>
��DB�
0X��7�u��ӥt�λ�m�ǏO�rb�Q@��,f������F@�An5&y;"��z�����߸a�+�ӳo���R�G��?��= �S��
�!�X.n�wș���kO��� �}��ݻ�ŋ�k�1��I����s�����Ν;Ӿ��ҁ����k��bAL(�FVG���"}ȝ�:�!٢�
"��	Lܘ�!�	S�����c80����v�m��/�`�C���ʲ�#-Xkd����,!��q���6 s�<ʟu
j��q,1����@��,j8�HF�E@r' � ����@�0P�x���<� �o7�@3eO>��a��������2�HE�4�'�� �Γ	��8#�w#�������u�|��kX��#�!�E�@�¹�9�GP4�kP]����8ه�13=�d�B�Q," 9�� �Z��" " "P�]�$��VD@D@r$ � �Z��" " "P%�U�" " "�#9֚d���0(	���	�0ȱ�$������D@�AI`�������H@�A��&�E@D@D�$2J�lE@D@D G2r�5�," " %�aPXe+" " 9�a�c�If(�����*[ȑ��kM2�����@Id�Vي����@�d�Xk�YD@D@J" à$��VD@D@r$ � �Z��" " "P%�U�" " "�#9֚d���0(	���	�0ȱ�$������D@�AI`�������H@�A��&�E@D@D�$2J�lE@D@D G2r�5�," " %�aPXe+" " 9�a�c�If(�����*[ȑ��kM2�����@Id�Vي����@�d�Xk�YD@D@J" à$��VD@D@r$ � �Z��" " "P%�U�" " "�#9֚d���0(	���	�0ȱ�$������D@�AI`�������H@�A��&�E@D@D�$2J�lE@D@D G2r�5�," " %�aPXe+" " 9�a�c�If(�����*[ȑ��kM2�����@Id�Vي����@�d�Xk�YD@D@J" à$��VD@D@r$ � �Z��" " "P%�U�" " "�#9֚d���0(	���	�0ȱ�$������D@�AI`�������H@�A��&�E@D@D�$2J�lE@D@D G2r�5�," " %�aPXe+" " 9�a�c�If(�����*[ȑ��kM2�����@Id�Vي����@�d�Xk�YD@D@J" à$��VD@D@r$ � �Z��" " "P%�U�" " "�#9֚d���0(	���	�0ȱ�$������D@�AI`�������H@�A��&�E@D@D�$2J�lE@D@D G2r�5�," " %��o���"z    IEND�B`�                                                                                                                                                                                                                                                                                                                                                                                            phjamf/jamf_testme.py                                                                               000644  000765  000024  00000000464 13647126320 015642  0                                                                                                    ustar 00smasud                          staff                           000000  000000                                                                                                                                                                         from jamf_connector import JamfConnector

jamf = JamfConnector()
jamf.config = {
    'base_url': 'https://tryitout.jamfcloud.com/JSSResource',
    'username': '',
    'password': '',
    'verify_server_cert': False
    }

jamf.initialize()

jamf.action_identifier = 'get_system_info'

jamf.handle_action({})
                                                                                                                                                                                                            phjamf/readme.html                                                                                  000640  000765  000024  00000000205 13645400575 015107  0                                                                                                    ustar 00smasud                          staff                           000000  000000                                                                                                                                                                         <html>
  <head></head>
  <body>Replace this text in the app's <b>readme.html</b> to contain more detailed information</body>
</html>
                                                                                                                                                                                                                                                                                                                                                                                           phjamf/state_file                                                                                   000644  000765  000024  00000000000 13647126434 015024  0                                                                                                    ustar 00smasud                          staff                           000000  000000                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         