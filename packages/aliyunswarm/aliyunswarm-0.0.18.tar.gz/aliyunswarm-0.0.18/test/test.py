from aliyunswarm import *

if __name__ == "__main__":
    swarm_api = SwarmApi("https://master2g4.cs-cn-shanghai.aliyun.com:20080/",
                        "./certFiles/ca.pem",
                        "./certFiles/cert.pem",
                        "./certFiles/key.pem")

    ################################################
    # applications api
    ################################################
    # 查询全部应用
    swarm_api.query_applications()
    # 查询应用
    swarm_api.query_applications('swarmtest')
    # 创建应用
    template = open('./compose/compose_ngx.yaml', 'r').read()
    swarm_api.create_application(template, 'swarmtest', 'swarm test')
    # 停止应用
    swarm_api.stop_application('swarmtest')
    # 启动应用
    swarm_api.start_application('swarmtest')
    # 终止应用
    swarm_api.kill_application('swarmtest')
    # 删除应用
    swarm_api.delete_application('swarmtest')
    # 重新部署应用
    swarm_api.redeploy_application('swarmtest')
    # 更新应用
    template = open('./compose/compose_ngx.yaml', 'r').read()
    swarm_api.update_application(template, 'swarmtest', 'swarmtest 2', version='2.0')

    ################################################
    # services api
    ################################################
    # 查询服务
    swarm_api.query_services('api')
    # # 查询指定应用的服务
    swarm_api.query_service('swarmtest', 'api')
    # # 启动指定应用的服务
    swarm_api.start_service('swarmtest', 'api')
    # # 停止指定应用的服务
    swarm_api.stop_service('swarmtest', 'api')
    # # 中止指定应用的服务
    swarm_api.kill_service('swarmtest', 'api')
