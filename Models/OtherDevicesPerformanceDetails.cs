using System;
using System.Collections.Generic;
using System.Text;

namespace BHL_cieplo.Models
{
    public class OtherDevicesPerformanceDetails
    {
        public TypeOfDay TypeOfDay { get; set; }
        public TimePeriod Period { get; set; }
        public int PowerConsumed { get; set; }
        public int PowerProduced { get; set; }

    }
}
