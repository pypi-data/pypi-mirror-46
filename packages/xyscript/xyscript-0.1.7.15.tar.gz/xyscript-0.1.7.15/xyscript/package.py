#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import os
import sys
import stat
import time
import threading
import time

from git import Repo

from xyscript.xylog import *
from xyscript.cert import Cert
from xyscript.CommonScript import IOSProjectTool
from xyscript.mail import Email
import xyscript.globalvar as gv

SELECT_FILE_COUNT = 0
WORK_SPACE = None

ENV_CHANGE_COUNT = 0


def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args) 
    # 守护 !!!
    t.setDaemon(True) 
    # 启动
    t.start()
    # 阻塞--卡死界面！
    # t.join()
class Package:
    
    def clone_form_address(self,address,local_path):

        from pathlib import Path
        folder_name = (address.split("/")[-1]).split(".")[0] +' ' + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

        try:
            #创建目录
            local_path = local_path + "/" + folder_name
            if Path(local_path).exists():
                warninglog(folder_name + "is exists")
            else:
                os.mkdir(local_path)
            
            try:
                os.chdir(local_path)
                warninglog("current workspace is: " + local_path)
            except BaseException as error:
                faillog("change worksapce failed")
                # Email(gv.get_value("NOTIFICATION_EMAILS")).send_package_email(False)
                sys.exit()
                
            # 更改权限
            os.chmod(local_path, stat.S_IRWXU)
            local_path = local_path + "/"
            Repo.clone_from(url=address, to_path=local_path, progress=None)
            successlog("clone project success")
        except BaseException as error:
            warninglog(format(error))

    def change_branch(self, branch_name, git=None):
        """
        change_branch
        """
        if git is None:
            repo = Repo(os.getcwd())
            # print(os.getcwd())
            print("start change branch to:",branch_name)
            local_branch_names = []#本地库列表
            remote_branch_names = []#远端库列表
            current_branch = repo.active_branch.name
            # print("current_branch_name:", current_branch)
            for localitem in repo.heads :
                local_branch_names.append(localitem.name)
                # print(localitem.name)
            # print("local_branch_names:", local_branch_names)

            for remoteitem in repo.refs:
                remote_branch_names.append(remoteitem.name)
                # print(remoteitem)
            # print("remote_branch_names:", remote_branch_names)

            if branch_name == current_branch:
                # print("就是当前分支，不需要切换")
                warningstring = "current branch is already :" + branch_name
                warninglog(warningstring)
            else:
                if branch_name in local_branch_names:
                    # print("本地存在目标分支，切换即可")
                    try:
                        local_target_branch = None
                        if branch_name == "develop":
                            local_target_branch = repo.heads.develop
                        elif branch_name == "Develop" :
                            local_target_branch = repo.heads.Develop
                        elif branch_name == "master" :
                            local_target_branch = repo.heads.master

                        repo.head.reference = local_target_branch
                        successlog("change branch success")
                    except BaseException as error:
                        errstr = "change branch failed:" + str(error)
                        faillog(errstr)
                        # Email(gv.get_value("NOTIFICATION_EMAILS")).send_package_email(False)
                        sys.exit()
                    
                else:
                    remote_branch_name = 'origin/' + branch_name
                    if remote_branch_name in remote_branch_names:
                        # print("远端存在目标分支同名分支，checkout")
                        try:
                            git = repo.git
                            git.checkout('-b', branch_name, remote_branch_name)
                            # repo.remote().pull()
                            successlog("change branch success")
                        except BaseException as error:
                            errstr = "checkout failed:" + str(error)
                            faillog(errstr)
                    else:
                        errstr = "have no branch named:" + branch_name + " exist,cannot to checkout"
                        # errstr = "\033[1;31m" + "远端不存在名为："+ branch_name + "的分支，无法checkout,请先创建远端仓库分支再checkout" + "\033[0m"
                        faillog(errstr)
                        # Email(gv.get_value("NOTIFICATION_EMAILS")).send_package_email(False)
                        sys.exit()

        else:
            print(branch_name)

    def pull_submodule(self):
        """
        pull submodules
        """
        try:
            currentPath = os.getcwd()
            repo = Repo(currentPath)
            initFlag = 0
            file = open("ProjConfig.json")
            moduleConfigList = json.load(file)
            for moduleConfig in moduleConfigList:
                module_path = currentPath + "/" + moduleConfig["module"]
                if not os.listdir(module_path):
                    initFlag = 1
            if initFlag == 1:
                print("submodule init...")
                repo.git.submodule('update', '--init')
                print("submodule init success")
            for moduleConfig in moduleConfigList:
                module_path = currentPath + "/" + moduleConfig["module"]
                sub_repo = Repo(module_path)
                sub_remote = sub_repo.remote()
                sub_repo.git.reset('--hard')
                sub_repo.git.checkout(moduleConfig["branch"])
                sub_remote.pull()
                print(module_path + " " + "\033[1;32m" +
                      moduleConfig["branch"] + "\033[0m" + " pull success")
        except BaseException as error:
            errorstr = "pull submodule failed:" + format(error)
            faillog(errorstr)
            # sys.exit()
    
    def change_default_net_env(self,env):
        from pbxproj import XcodeProject
        global ENV_CHANGE_COUNT

        # print(self._search_xcodeproj())
        filepath = self._search_xcodeproj() + "/project.pbxproj"
        print("start change default environment variable")

        file_data = ""
        with open(filepath,encoding="utf-8") as f:
            for line in f:
                if "SC_URL_TYPE =" in line:
                    # print(line,end="")
                    line = str.split(line,'SC_URL_TYPE')[0] + "SC_URL_TYPE = " + env +";\n"
                file_data += line

        with open(filepath,"w",encoding="utf-8") as f:
            f.write(file_data)

        

    def _search_xcodeproj(self):
        paths = os.listdir(os.getcwd())
        for filename in paths:
            if ".xcodeproj" in filename :
                return filename
        faillog("The current path does not have a: xcodeproj file,such as :projectname.xcodeproj")
        # Email(gv.get_value("NOTIFICATION_EMAILS")).send_package_email(False)
        sys.exit()

    def select_directory(self):
        global SELECT_FILE_COUNT

        import tkinter as tk
        from tkinter import filedialog
        
        root = tk.Tk()
        root.withdraw()
        root.update()
        file_path = filedialog.askdirectory(initialdir=os.getcwd(), title="选择项目存储的路径")

        SELECT_FILE_COUNT = SELECT_FILE_COUNT + 1
        if SELECT_FILE_COUNT >=3:
            faillog("you have give up choosing an folder three times!")
            # Email(gv.get_value("NOTIFICATION_EMAILS")).send_package_email(False)
            sys.exit()
        if file_path == "":
            warninglog("please choose an folder")
            self.select_directory()
        else:
            root.update()
            # root.mainloop()
            return file_path

    def _get_project_version(self):
        filepath = self._search_xcodeproj() + "/project.pbxproj"
        # print("start change default environment variable")

        # file_data = ""
        with open(filepath,encoding="utf-8") as f:
            for line in f:
                print(line)
    
    def package_to_platform(self,platform=None, project_version=None, project_build=None, emails=None):
        """
        配置证书 等效于 fastlane + platform
        """
        #获取项目当前version、build

        if platform == None:
            platform = "pgyer"
            
        
        version_str = ""
        build_str = ""
        if project_version != None:
            version_str = " version:" + project_version
        
        if project_build != None:
            build_str = " build:" + project_build

        
        print("start package to " + platform)
        if Cert().fastlane_is_in_gem() or Cert().fastlane_is_in_brew() :
            shell_str = "fastlane package" + platform + version_str + build_str
            try:
                if Cert()._have_fastfile():
                    result = os.popen(shell_str)
                    text = result.read()
                    print(text)
                    if "fastlane.tools just saved" in text:
                        successlog("package to " + platform + " success")
                    else:
                        faillog("package to " + platform + " failed")

                    result.close()
                    # Email(gv.get_value("NOTIFICATION_EMAILS")).send_package_email(True)
                else:
                    faillog("You may not have the fastfile,please set fastlane up first!")
                    # Email(gv.get_value("NOTIFICATION_EMAILS")).send_package_email(False)
                    sys.exit()
                
            except BaseException  as error:
                faillog(str(error))
                # Email(gv.get_value("NOTIFICATION_EMAILS")).send_package_email(False)
                sys.exit()
        else:
            warninglog("You may not have the fastlane installed yet,autoinstall now...")
            Cert()._install_fastlane()
            self.package_to_platform(platform,project_version,project_build)

    def auto_package(self, project_address=None, branch_name=None, platform=None, net_env=None, project_version=None, project_build=None,emails=None):
        if branch_name == None:
            branch_name = "Develop"
        if platform == None:
            platform = "pgyer"
        if emails == None:
            emails = []

        print("自动打包 项目：",project_address,"\n分支为：",branch_name,"\n发布平台为：",platform,"\n网络环境：",net_env,"\n版本号：",project_version,"\n编译号：",project_build)
        print("please choose an folder")
        
        # #clone
        # self.clone_form_address(project_address,self.select_directory())
        self.clone_form_address(project_address,os.getcwd())
        # #切换分支
        self.change_branch(branch_name)
        # #拉子模块
        self.pull_submodule()
        # #pod indtall
        IOSProjectTool().run_pod_install()
        # #选择网络环境
        if net_env != None:
            self.change_default_net_env(net_env)
        # #fastlane syn
        # Cert().run_cert_syn()
        # #安装 pgyer 插件
        os.system("bundle install")
        # #打包
        self.package_to_platform(platform, project_version, project_build,emails)

    def init_project(self, project_address=None, branch_name=None, platform=None, net_env=None):
        if branch_name == None:
            branch_name = "Develop"
        if platform == None:
            platform = "pgyer"

        print("initial 项目：",project_address," 分支为：",branch_name," 发布平台为：",platform,"网络环境：",net_env)
        print("please choose an folder")
        
        # #clone
        self.clone_form_address(project_address,self.select_directory())
        # #切换分支
        self.change_branch(branch_name)
        # #拉子模块
        self.pull_submodule()
        # #pod indtall
        IOSProjectTool().run_pod_install()
        # #选择网络环境
        if net_env != None:
            self.change_default_net_env(net_env)
        # #fastlane syn
        Cert().run_cert_syn()

if __name__ == "__main__":
    # Package().change_default_net_env("dev")
    Package()._get_project_version()
