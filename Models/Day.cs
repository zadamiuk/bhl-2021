using System.Collections.Generic;

namespace BHL_cieplo.Models
{
    public class Day
    {
        public TypeOfDay TypeOfDay { get; set; }
        public List<TimePeriod> MyProperty { get; set; }
    }
}