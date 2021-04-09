using System;
using System.Collections.Generic;
using System.Text;

namespace BHL_cieplo.Models
{
    class ExpectedTemperaturesDetails
    {
        public TypeOfDay TypeOfDay { get; set; }
        public TimePeriod TimePeriod { get; set; }
        public int Temperature { get; set; }
    }
}
