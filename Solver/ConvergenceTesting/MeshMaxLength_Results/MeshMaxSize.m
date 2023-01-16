sizes = ["1.0e-6","7.5e-7","5.0e-7","2.5e-7","1.0e-7"];
size_value = [1e-6,7.5e-7, 5e-7, 2.5e-7,1e-7]/1e-9;
for ii = 1:length(sizes)-1
    size = 0.5e-6 + ii*0.5e-6;
    filename = "MeshMax" + string(sizes(ii)) +  ".mat";
    data = load(filename);
    x0 = data.lum.x0;
    y0 = data.lum.y0;
    x1 = data.lum.x1;
    y1 = data.lum.y1;
    figure(1)
    plot(x0,y0)
    hold on
    figure(2)
    scatter(size_value(ii),y0(1),'r')
    scatter(size_value(ii),y1(1),'b')
    hold on

end

figure(1)
xlabel('Voltage [V]')
ylabel('total_charge_p')

figure(2)
xlabel('Maximum mesh size [nm]')
ylabel('total charge at V=0')
legend('n', 'p')