# 删除旧的安装包
write-output "删除旧的安装包"
Remove-Item dist/*

# 更新元数据
python .\meta_modify.py test

# 封包
python -m build

# API token
# 测试服
Write-Output "上传到测试服"
python -m twine upload --repository testpypi dist/* --verbose

exit 0 # 提前退出脚本


# 延迟一段时间
$delay = 90
Write-Output "暂停 $delay 秒，等待测试服更新"
# Start-Sleep -Seconds $delay
for ($i = 0; $i -lt $delay; $i ++) {
    $left = $delay - $i
    Write-Progress -Activity "等待 $delay 秒" -Status "还有 $left 秒" -PercentComplete ($i / $delay * 100)
    # Write-Output "还有 $left 秒"
    Start-Sleep -Seconds 1
    
}

# 更新测试包
Write-Output "更新测试包"
conda activate cst-2024
pip install -i https://test.pypi.org/simple/ --upgrade mzcst-2024