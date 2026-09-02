@echo off
cd /d C:\Users\Auriseg\jit-global-pages
wscript //B C:\Users\Auriseg\jit-global\_interval_force_deploy.vbs
echo Ran VBS deploy. See _deploy_status.txt
type C:\Users\Auriseg\jit-global-pages\_deploy_status.txt
