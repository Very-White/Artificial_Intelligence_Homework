clc,clear,close all
%画出城市
cities_position=readtable('cities_position.xlsx');
cities_position=table2array(cities_position(:,2:3));
scatter(cities_position(:,1),cities_position(:,2),'MarkerFaceColor','#EDB120','MarkerEdgeColor','#A2142F','LineWidth',1,'DisplayName','城市')
xlabel('城市的x坐标')
ylabel('城市的y坐标')
grid on
legend show
%给城市连线，创建一个动图
hold on
paths_and_length=readtable('退火模拟算法.xlsx');
paths_and_length=table2array(paths_and_length);
paths=paths_and_length(:,1:size(paths_and_length,2)-1);%刚好少一列
paths=paths+1;%给所有城市的索引下标加+1
for i=1:size(paths_and_length,1)
    %用paths做索引，画出第i行的路径
    x_position=cities_position(paths(i,:),1);
    y_position=cities_position(paths(i,:),2);
    line=plot(x_position,y_position,'k-.','DisplayName','路径');
    title(['迭代次数:',num2str(i)])
    pause(0.025)
    if i~=size(paths_and_length,1)
        delete(line)
    end
end
hold off
%画出路径长度的变化
length=paths_and_length(:,size(paths_and_length,2));
figure
title('路径长度随迭代次数变化曲线')
plot(1:size(length),length,'DisplayName','路径长度')
xlabel('迭代次数')
ylabel('路径长度')
grid on
legend show
