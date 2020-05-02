using System.IO;
using WebWindows;

namespace Dynatron.Core {
    internal class Program {
        private static readonly string m_EntryPoint = "Web/build/index.html";
        private static WebWindow m_Window;
        static void Main(string[] args) {
            m_Window = new WebWindow("Dynatron Server");

            if (File.Exists(m_EntryPoint)) {
                m_Window.NavigateToLocalFile(m_EntryPoint);
            }

            m_Window.WaitForExit();
        }
    }
}
