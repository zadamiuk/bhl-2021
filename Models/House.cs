using System;
using System.Collections.Generic;
using System.Reflection.Metadata.Ecma335;
using System.Text;

namespace BHL_cieplo.Models
{
    public class House
    {
        public int CurrentTemperature { get; set; }
        public int GoalTemperature { get; set; }
        public int EnergyInput { get; set; }
        public int EnergyDemand { get; set; }
        public Boiler Boiler { get; set; }
        public EnergyMode EnergyMode { get; set; }
    }
}
