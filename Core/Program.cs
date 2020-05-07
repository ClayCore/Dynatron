using System;
using SpiderEye;
using SpiderEye.Windows;

namespace Dynatron.Core {
    public abstract class ProgramBase {
        protected static void Run() {
            using (var window = new Window()) {
                //window.EnableDevTools = true;

                Application.ContentProvider = new EmbeddedContentProvider("Client\\build\\debug");

                Application.Run(window, "/index.html");
            }
        }
    }

    internal class Program : ProgramBase {

        [STAThread]
        static void Main(string[] args) {
            WindowsApplication.Init();
            Run();
        }
    }
}
