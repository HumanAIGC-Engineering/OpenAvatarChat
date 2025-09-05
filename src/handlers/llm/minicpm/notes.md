由于MiniCPM仓库相对较大，我们不再将其作为子模块引入，以免影响不使用该功能用户的拉取效率。如果需要该模块，请从 https://github.com/OpenBMB/MiniCPM-V/tree/06be4aa3d23fbb135adc7e532b961317868e02ee 下载对应版本的代码，并解压到MiniCPM-o目录下。参考命令如下：

For the size of MiniCPM repository, we decide not directly include it as a submodule to reduce the overall clone time. If this module is needed, the related code can be downloaded from https://github.com/OpenBMB/MiniCPM-V/tree/06be4aa3d23fbb135adc7e532b961317868e02ee and extracted into the folder MiniCPM-o under this folder. Following command can be tried as an example.
```
wget https://github.com/OpenBMB/MiniCPM-V/archive/06be4aa3d23fbb135adc7e532b961317868e02ee.zip -O MiniCPM-o.zip
unzip MiniCPM-o.zip -d .
mv MiniCPM-V-06be4aa3d23fbb135adc7e532b961317868e02ee MiniCPM-o
```