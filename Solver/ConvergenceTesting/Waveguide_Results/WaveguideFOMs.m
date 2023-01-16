basename = "NoBumper";
basename2 = "Bumper";
basename3 = "BumperBigMeshRegion";
ext = ".mat";
contacts = [100,150,200,250,300,350,400,450,500,550,600,650,700,750,800,850,900,950,1000];
V = linspace(0,5,21);
for ii =1:length(contacts)
    data= load(basename + string(ii) + ext);
    data_bumper= load(basename2 + string(ii) + ext);
    data_bumperMesh = load(basename3 + string(ii) + ext);
    neff_real = data.neff_real;
    neff_imag = data.neff_imag;
    
    neff_real_bumper = data_bumper.neff_real;
    neff_imag_bumper = data_bumper.neff_imag;
    
    neff_real_bumper_mesh = data_bumperMesh.neff_real;
    neff_imag_bumper_mesh = data_bumperMesh.neff_imag;
    dneff_real = data.dneff_real;
    phase = data.phase;
    phase_bumper = data_bumper.phase;
    phase_bumper_mesh = data_bumperMesh.phase;
    figure(1)
    plot(V,neff_real)
    hold on
    figure(2)
    plot(V,neff_imag)
    hold on
    figure(3)
    scatter(contacts(ii), neff_real(1), 'b')
    hold on
    scatter(contacts(ii), neff_real_bumper(1), 'r')
    scatter(contacts(ii), neff_real_bumper_mesh(1), 'g')
    figure(4)
    scatter(contacts(ii), neff_imag(1), 'b')
    hold on
    scatter(contacts(ii), neff_imag_bumper(1), 'r')
    scatter(contacts(ii), neff_imag_bumper_mesh(1), 'g')
    
    figure(5)
    plot(V,dneff_real)
    hold on
    figure(6)
    plot(V, phase, 'r')
    hold on
    plot(V, phase_bumper, 'b')
    plot(V,phase_bumper_mesh,'g')

    
end
figure(1)
xlabel('Voltage [V]')
ylabel('n_{eff}')
legend('100nm','150nm','200nm','250nm','300nm','350nm','400nm','450nm','500nm')
figure(2)
xlabel('Voltage [V]')
ylabel('n_{imag}')
legend('100nm','150nm','200nm','250nm','300nm','350nm','400nm','450nm','500nm')
figure(3)
xlabel('N++/P++ Size at V=0 [nm]')
ylabel('n_{eff}')
legend('NoBumper','Bumper')
figure(4)
xlabel('N++/P++ Size at V=0 [nm]')
ylabel('n_{imag}')
legend('NoBumper','Bumper')